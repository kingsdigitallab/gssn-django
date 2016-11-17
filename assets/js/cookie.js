define([
    'module',
    'jquery',
    'jscookie'
], function(module, $, cookie) {
    'use strict';

    $(document).ready(function() {
        if (!cookie.get('gssn-cookie')) {
            $("#cookie-disclaimer").removeClass('hide');
        }
        // Set cookie
        $('#cookie-disclaimer .closeme').on("click", function() {
            cookie.set('gssn-cookie', 'gssn-cookie-set', { expires: 30 });
        });
    });

    return module;
});
