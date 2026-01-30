from odoo import fields, models, api
from odoo.exceptions import ValidationError
from lxml import etree
import ast
import json

MAX_SIZE_KB = 500
MAX_IMAGE_SIZE_BYTES = MAX_SIZE_KB * 1024
INSTRUCTION_TEXT = f"PNG/SVG only (max {MAX_SIZE_KB}KB)."


class PosConfig(models.Model):
    _inherit = "pos.config"

    storrd_saver_screen_img = fields.Binary(
        string="Lock Screen Logo",
        help=INSTRUCTION_TEXT,
    )

    storrd_saver_screen_img_name = fields.Char(string="Logo Filename")

    storrd_saver_instructions = fields.Char(compute="_compute_storrd_instructions")

    @api.depends("storrd_saver_screen_img")
    def _compute_storrd_instructions(self):
        """Generates dynamic instructions for the UI based on global constants."""
        for config in self:
            config.storrd_saver_instructions = INSTRUCTION_TEXT

    @api.constrains("storrd_saver_screen_img")
    def _check_saver_screen_img(self):
        """Validates that the uploaded image size does not exceed max KB and the format is PNG or SVG."""
        for config in self:
            if config.storrd_saver_screen_img:
                file_size = len(config.storrd_saver_screen_img) * 3 / 4
                if file_size > MAX_IMAGE_SIZE_BYTES:
                    raise ValidationError(f"The image is too large! {INSTRUCTION_TEXT}")

                if config.storrd_saver_screen_img_name:
                    extension = config.storrd_saver_screen_img_name.split(".")[
                        -1
                    ].lower()
                    if extension not in ["png", "svg"]:
                        raise ValidationError(
                            f"Unsupported file format! {INSTRUCTION_TEXT}"
                        )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_storrd_saver_screen_img = fields.Binary(
        related="pos_config_id.storrd_saver_screen_img",
        readonly=False,
        string="Lock Screen Logo",
    )

    pos_storrd_saver_instructions = fields.Char(
        related="pos_config_id.storrd_saver_instructions",
        readonly=True,
    )

    pos_storrd_saver_screen_img_name = fields.Char(
        related="pos_config_id.storrd_saver_screen_img_name",
        readonly=False,
    )

    @api.onchange("pos_storrd_saver_screen_img")
    def _onchange_storrd_saver_screen_img(self):
        """Validates file size and extension immediately and clears fields if validation fails."""
        if self.pos_storrd_saver_screen_img:
            file_size = len(self.pos_storrd_saver_screen_img) * 3 / 4
            extension = ""
            if self.pos_storrd_saver_screen_img_name:
                extension = self.pos_storrd_saver_screen_img_name.split(".")[-1].lower()

            if file_size > MAX_IMAGE_SIZE_BYTES or (
                extension and extension not in ["png", "svg"]
            ):
                self.pos_storrd_saver_screen_img = False
                self.pos_storrd_saver_screen_img_name = False
                return {
                    "warning": {
                        "title": "Invalid File",
                        "message": f"Please upload a valid file. {INSTRUCTION_TEXT}",
                    }
                }
        else:
            self.pos_storrd_saver_screen_img_name = False

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """Injects max_file_size and accepted_file_extensions into the XML view modifiers."""
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form" and res.get("xml_id") == "point_of_sale.res_config_settings_view_form":
            doc = etree.fromstring(res["arch"])

            for node in doc.xpath("//field[@name='pos_storrd_saver_screen_img']"):
                opt = ast.literal_eval(node.get("options", "{}"))
                opt.update({
                    "max_file_size": MAX_SIZE_KB,
                    "accepted_file_extensions": ".png,.svg",
                })
                node.set("options", json.dumps(opt))

            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
