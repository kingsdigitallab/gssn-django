define([
    'module',
    'jquery',
    'slick'
], function(module, $) {
    'use strict';

    $(document).ready(function() {

        $('.slider-home').slick({
            autoplay: true,
            autoplaySpeed: 6000
        });

        $('.slider-for').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            adaptiveHeight: true,
            arrows: false,
            fade: true,
            asNavFor: '.slider-nav'
        });
        $('.slider-nav').slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            asNavFor: '.slider-for',
            dots: true,
            centerMode: true,
            variableWidth: true,
            focusOnSelect: true,
            lazyLoad: 'ondemand'
        });
    });

    return module;
});
