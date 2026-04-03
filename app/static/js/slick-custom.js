(function ($) {
    "use strict";

    /*=========================================
    [ Slick1 – Home Banner ]
    =========================================*/
    $('.wrap-slick1').each(function () {
        var wrapSlick1 = $(this);
        var slick1 = $(this).find('.slick1');

        var itemSlick1 = slick1.find('.item-slick1');
        var layerSlick1 = slick1.find('.layer-slick1');
        var actionSlick1 = [];

        slick1.on('init', function () {
            var layerCurrentItem = $(itemSlick1[0]).find('.layer-slick1');

            actionSlick1.forEach(clearTimeout);
            actionSlick1 = [];

            layerSlick1.removeClass(function () {
                return $(this).data('appear') + ' visible-true';
            });

            layerCurrentItem.each(function (i) {
                actionSlick1[i] = setTimeout(() => {
                    $(this).addClass($(this).data('appear') + ' visible-true');
                }, $(this).data('delay'));
            });
        });

        slick1.slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    fade: true,
    infinite: true,
    autoplay: true,
    autoplaySpeed: 6000,
    speed: 1000,
    arrows: true,
    pauseOnFocus: false,
    pauseOnHover: false,

    appendArrows: wrapSlick1,
    prevArrow: '<button class="arrow-slick1 prev-slick1"><i class="zmdi zmdi-caret-left"></i></button>',
    nextArrow: '<button class="arrow-slick1 next-slick1"><i class="zmdi zmdi-caret-right"></i></button>',

    dots: wrapSlick1.find('.wrap-slick1-dots').length > 0,
    appendDots: wrapSlick1.find('.wrap-slick1-dots'),
    dotsClass: 'slick1-dots',

    // ✅ THIS IS THE KEY FIX
    customPaging: function (slick, index) {
        var thumb = $(slick.$slides[index]).data('thumb');
        var caption = $(slick.$slides[index]).data('caption');

        return `
            <img src="${thumb}">
            <span class="caption-dots-slick1">${caption}</span>
        `;
    }
});

        slick1.on('afterChange', function (e, slick, currentSlide) {
            var layerCurrentItem = $(itemSlick1[currentSlide]).find('.layer-slick1');

            actionSlick1.forEach(clearTimeout);
            actionSlick1 = [];

            layerSlick1.removeClass(function () {
                return $(this).data('appear') + ' visible-true';
            });

            layerCurrentItem.each(function (i) {
                actionSlick1[i] = setTimeout(() => {
                    $(this).addClass($(this).data('appear') + ' visible-true');
                }, $(this).data('delay'));
            });
        });
    });

    /*=========================================
    [ Slick2 – Related Products ]
    =========================================*/
    $('.wrap-slick2').each(function () {
        $(this).find('.slick2').slick({
            slidesToShow: 4,
            slidesToScroll: 4,
            infinite: false,
            autoplay: false,
            arrows: true,
            appendArrows: $(this),
            prevArrow: '<button class="arrow-slick2 prev-slick2"><i class="fa fa-angle-left"></i></button>',
            nextArrow: '<button class="arrow-slick2 next-slick2"><i class="fa fa-angle-right"></i></button>',
            responsive: [
                { breakpoint: 1200, settings: { slidesToShow: 4, slidesToScroll: 4 } },
                { breakpoint: 992, settings: { slidesToShow: 3, slidesToScroll: 3 } },
                { breakpoint: 768, settings: { slidesToShow: 2, slidesToScroll: 2 } },
                { breakpoint: 576, settings: { slidesToShow: 1, slidesToScroll: 1 } }
            ]
        });
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $($(e.target).attr('href')).find('.slick2').slick('refresh');
    });

    /*=========================================
    [ Slick3 – Product Detail Images ]
    =========================================*/
    $('.wrap-slick3').each(function () {
        var slick3 = $(this).find('.slick3');

        if (slick3.hasClass('slick-initialized')) {
            slick3.slick('unslick');
        }

        slick3.slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            fade: true,
            infinite: true,
            autoplay: false,
            arrows: true,
            dots: true,
            appendArrows: $(this).find('.wrap-slick3-arrows'),
            appendDots: $(this).find('.wrap-slick3-dots'),
            dotsClass: 'slick3-dots',
            prevArrow: '<button class="arrow-slick3 prev-slick3"><i class="fa fa-angle-left"></i></button>',
            nextArrow: '<button class="arrow-slick3 next-slick3"><i class="fa fa-angle-right"></i></button>',
            customPaging: function (slick, index) {
                var thumb = $(slick.$slides[index]).data('thumb');
                return `<img src="${thumb}"><div class="slick3-dot-overlay"></div>`;
            }
        });
    });

})(jQuery);
