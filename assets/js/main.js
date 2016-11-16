// Main
require([
    'requirejs',
    'jquery',
    'fn',
    'js-cookie',
    'ga',
    'sl'
], function(r, $) {
    'use strict';

    $(document).ready(function() {
        $('.gssn-icon-search').bind("click", function() {
            $('.gssn-search').addClass("gssn-search-open");
            return false;
        });

        // Set cookie
        $('#cookie-disclaimer .closeme').on("click", function() {
            Cookies.set('name', 'gssn-cookie', { expires: 30 });
            return true;
        });
    });
});