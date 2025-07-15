odoo.define(
    "custom_filter_groupby_visibility_control.web.CustomFilterItemPatch",
    function (require) {
        const session = require("web.session");
        const CustomFilterItem = require("web.CustomFilterItem");
        const {patch} = require("web.utils");
        const {hooks, useState} = owl;
        const {onWillStart} = hooks;

        patch(
            CustomFilterItem.prototype,
            "custom_filter_groupby_visibility_control.CustomFilterItemPatch",
            {
                setup() {
                    this._super.apply(this, arguments);
                    this.visibleState = useState({isVisible: true});

                    onWillStart(async () => {
                        const hasAccess = await session.user_has_group(
                            "custom_filter_groupby_visibility_control.custom_filter_groupby_access"
                        );
                        this.visibleState.isVisible = hasAccess;
                    });
                },
            }
        );
    }
);
