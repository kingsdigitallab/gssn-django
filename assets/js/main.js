// Main
require([
    'requirejs',
    'jquery',
    'fn',
    'ga',
    'sl'
], function(r, $) {
    'use strict';

    $(document).ready(function() {

	    // $('toggle').click(function () {
	    //     var trigger = $(this),
	    //         inputForm = trigger.siblings('#searchform'),
	    //         expanded = inputForm.is("expanded")

	    //         if (expanded) {
	    //             inputForm.removeClass('expanded').animate({
	    //                 right: 100
	    //             })
	    //         } else {
	    //             inputForm.animate({
	    //                 right: 48
	    //             }, function () {
	    //                 inputForm.addClass('expanded').find('input').focus()
	    //             })
	    //         }
	    // })

	    $(".form input").blur(function () {
	        $(this).closest('.form').find('.toggle').click()
	    })

    });
});
