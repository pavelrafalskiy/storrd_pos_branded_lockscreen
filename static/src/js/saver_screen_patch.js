import { patch } from "@web/core/utils/patch";
import { SaverScreen } from "@point_of_sale/app/screens/saver_screen/saver_screen";
import { useService } from "@web/core/utils/hooks";

patch(SaverScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = useService("pos");
    },
});