import { patch } from "@web/core/utils/patch";
import { BinaryField } from "@web/views/fields/binary/binary_field";
import { useService } from "@web/core/utils/hooks";


patch(BinaryField.prototype, {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
    },

    async onFileChanged(ev) {
        const file = ev.target.files[0];
        const maxSizeKb = this.props.options?.max_file_size;
        const acceptedExtensions = this.props.acceptedFileExtensions || this.props.options?.accepted_file_extensions;

        if (file) {
            if (maxSizeKb && file.size > maxSizeKb * 1024) {
                this.notification.add(`File is too large! Max allowed size is ${maxSizeKb}KB.`, {
                    title: "Validation Error",
                    type: "danger",
                });
                ev.target.value = "";
                return;
            }

            if (acceptedExtensions && acceptedExtensions !== "*") {
                const fileName = file.name.toLowerCase();
                const extensions = acceptedExtensions.split(',').map(ext => ext.trim().toLowerCase());
                const isValid = extensions.some(ext => {
                    if (ext.startsWith('.')) return fileName.endsWith(ext);
                    if (ext.includes('/')) return file.type.match(new RegExp(ext.replace('*', '.*')));
                    return false;
                });

                if (!isValid) {
                    this.notification.add(`Invalid format! Allowed: ${acceptedExtensions}`, {
                        title: "Validation Error",
                        type: "danger",
                    });
                    ev.target.value = "";
                    return;
                }
            }
        }

        return super.onFileChanged(ev);
    }
});