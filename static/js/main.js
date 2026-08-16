// Глобальная вспомогательная функция копирования в буфер
window.copyToClipboard = function(text, successCallback) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(successCallback).catch(function() {
            prompt("Скопируйте ссылку:", text);
        });
    } else {
        prompt("Скопируйте ссылку:", text);
    }
};

// Функция специально для плашки в шапке (header-browser-warning)
window.copyHeaderPaymentLink = function(btnElement) {
    var $btn = jQuery(btnElement);
    var $textSpan = $btn.find('.btn-text');
    var originalText = $textSpan.length ? $textSpan.text() : $btn.text();

    // Берем текущий URL страницы (или заданный атрибут data-url)
    var urlToCopy = $btn.attr('data-url') || window.location.href;

    window.copyToClipboard(urlToCopy, function() {
        if ($textSpan.length) {
            $textSpan.text('✅ Ссылка скопирована!');
        } else {
            $btn.text('✅ Ссылка скопирована!');
        }
        setTimeout(function() {
            if ($textSpan.length) {
                $textSpan.text(originalText);
            } else {
                $btn.text(originalText);
            }
        }, 3000);
    });
};

AOS.init({
    duration: 800,
    easing: 'slide',
    once: true
});

jQuery(document).ready(function($) {
    "use strict";

    // -------------------------------------------------------------
    // 1. Мобильное меню
    // -------------------------------------------------------------
    var siteMenuClone = function() {
        $('.js-clone-nav').each(function() {
            var $this = $(this);
            $this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
        });

        $('.site-mobile-menu .has-children').each(function(index) {
            var $this = $(this);
            $this.prepend('<span class="arrow-collapse collapsed"></span>');

            $this.find('.arrow-collapse').attr({
                'data-toggle': 'collapse',
                'data-target': '#collapseItem' + index
            });

            $this.find('> ul').attr({
                'class': 'collapse',
                'id': '#collapseItem' + index
            });
        });

        $('body').on('click', '.js-menu-toggle, .site-mobile-menu-close', function(e) {
            e.preventDefault();
            $('body').toggleClass('offcanvas-menu');
            $('.js-menu-toggle').toggleClass('active', $('body').hasClass('offcanvas-menu'));
        });

        $('body').on('click', '.arrow-collapse', function(e) {
            e.preventDefault();
            $(this).toggleClass('active');
        });

        $(window).resize(function() {
            if ($(this).width() > 768) {
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                    $('.js-menu-toggle').removeClass('active');
                }
            }
        });

        $(document).mouseup(function(e) {
            var container = $(".site-mobile-menu");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                    $('.js-menu-toggle').removeClass('active');
                }
            }
        });
    };
    siteMenuClone();

    // -------------------------------------------------------------
    // 2. Слайдеры и Плагины
    // -------------------------------------------------------------
    var siteCarousel = function() {
        if (!$.fn.owlCarousel) return;

        if ($('.nonloop-block-13').length > 0) {
            $('.nonloop-block-13').owlCarousel({
                center: false,
                items: 1,
                loop: true,
                stagePadding: 0,
                margin: 0,
                autoplay: true,
                nav: true,
                navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
                responsive: {
                    600: { items: 2 },
                    1000: { items: 3 },
                    1200: { items: 4 }
                }
            });
        }

        if ($('.nonloop-block-14').length > 0) {
            $('.nonloop-block-14').owlCarousel({
                center: false,
                items: 1,
                loop: true,
                stagePadding: 30,
                margin: 0,
                autoplay: true,
                smartSpeed: 1000,
                nav: true,
                navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
                responsive: {
                    600: { margin: 20, items: 2 },
                    1000: { margin: 30, items: 2 },
                    1200: { margin: 30, items: 3 }
                }
            });
        }

        if ($('.slide-one-item').length > 0) {
            $('.slide-one-item').owlCarousel({
                center: false,
                items: 1,
                loop: true,
                stagePadding: 0,
                margin: 0,
                autoplay: true,
                pauseOnHover: false,
                nav: true,
                navText: ['<span class="icon-keyboard_arrow_left">', '<span class="icon-keyboard_arrow_right">']
            });
        }
    };
    siteCarousel();

    var siteStellar = function() {
        if ($.fn.stellar) {
            $(window).stellar({
                responsive: false,
                parallaxBackgrounds: true,
                parallaxElements: true,
                horizontalScrolling: false,
                hideDistantElements: false,
                scrollProperty: 'scroll'
            });
        }
    };
    siteStellar();

    var siteCountDown = function() {
        if ($.fn.countdown && $('#date-countdown').length > 0) {
            $('#date-countdown').countdown('2020/10/10', function(event) {
                $(this).html(event.strftime(''
                    + '<span class="countdown-block"><span class="label">%w</span> weeks </span>'
                    + '<span class="countdown-block"><span class="label">%d</span> days </span>'
                    + '<span class="countdown-block"><span class="label">%H</span> hr </span>'
                    + '<span class="countdown-block"><span class="label">%M</span> min </span>'
                    + '<span class="countdown-block"><span class="label">%S</span> sec</span>'));
            });
        }
    };
    siteCountDown();

    var siteDatePicker = function() {
        if ($.fn.datepicker && $('.datepicker').length > 0) {
            $('.datepicker').datepicker();
        }
    };
    siteDatePicker();

    var siteSticky = function() {
        if ($.fn.sticky && $('.js-sticky-header').length > 0) {
            $(".js-sticky-header").sticky({ topSpacing: 0 });
        }
    };
    siteSticky();

    // -------------------------------------------------------------
    // 3. Навигация и Скролл
    // -------------------------------------------------------------
    var OnePageNavigation = function() {
        $("body").on("click", ".main-menu li a, .smoothscroll, .site-mobile-menu .site-nav-wrap li a", function(e) {
            var href = $(this).attr('href');

            if (href && href.startsWith('#') && href !== '#') {
                e.preventDefault();
                var target = $(href);
                if (target.length) {
                    $('html, body').animate({
                        'scrollTop': target.offset().top
                    }, 600, 'easeInOutCirc', function() {
                        window.location.hash = href;
                    });
                }

                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                    $('.js-menu-toggle').removeClass('active');
                }
            } else if (href && href !== '#') {
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                    $('.js-menu-toggle').removeClass('active');
                }
            }
        });
    };
    OnePageNavigation();

    var siteScroll = function() {
        $(window).scroll(function() {
            var st = $(this).scrollTop();
            if (st > 100) {
                $('.js-sticky-header').addClass('shrink');
            } else {
                $('.js-sticky-header').removeClass('shrink');
            }
        });
    };
    siteScroll();

    $('.animated-item').each(function(index) {
        $(this).css('opacity', 0).delay(index * 200).animate({ opacity: 1 }, 500);
    });

    // -------------------------------------------------------------
    // 4. Модальные окна и ссылки оплаты
    // -------------------------------------------------------------
    $('.btn-open-pay-modal').on('click', function() {
        var payUrl = $(this).attr('data-pay-url') || $(this).data('pay-url');
        $('#modalProceedBtn').attr('href', payUrl);
    });

    $('#modalCopyBtn').on('click', function(e) {
        e.preventDefault();
        var linkToCopy = $('#modalProceedBtn').attr('href');

        if (!linkToCopy || linkToCopy === '#') {
            alert('Ссылка не найдена!');
            return;
        }

        var $btn = $(this);
        var originalText = $btn.text();

        window.copyToClipboard(linkToCopy, function() {
            $btn.text('✅ Ссылка скопирована!');
            setTimeout(function() { $btn.text(originalText); }, 3000);
        });
    });

    // -------------------------------------------------------------
    // 5. Обработка Всплывающих Popover в карточках
    // -------------------------------------------------------------
    $('body').on('click', '.close-popover-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).closest('.payment-hover-popover').addClass('is-closed');
    });

    $('body').on('click', '.btn-popover-copy', function(e) {
        e.preventDefault();
        var payUrl = $(this).attr('data-url');
        var $btn = $(this);
        var originalText = $btn.text();

        if (payUrl) {
            window.copyToClipboard(payUrl, function() {
                $btn.text('ССЫЛКА СКОПИРОВАНА! ✓');
                setTimeout(function() { $btn.text(originalText); }, 2500);
            });
        }
    });
});
