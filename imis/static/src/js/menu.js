odoo.define('agf.ComplementMenu', function(require) {
    "use strict";
    var UserMenu = require('web.UserMenu');
    var ComplementMenu = UserMenu.include({
        _onMenuSupport: function () {
            window.open('https://www.opensystechnologies.com', '_blank');
        },
    });
    return ComplementMenu;
});