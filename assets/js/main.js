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
    });
});