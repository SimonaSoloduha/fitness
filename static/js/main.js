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

        // Создаем стрелочки для выпадающих списков
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

        // Переключение мобильного меню (единый обработчик)
        $('body').on('click', '.js-menu-toggle, .site-mobile-menu-close', function(e) {
            e.preventDefault();
            $('body').toggleClass('offcanvas-menu');
            $('.js-menu-toggle').toggleClass('active', $('body').hasClass('offcanvas-menu'));
        });

        // Раскрытие подпунктов
        $('body').on('click', '.arrow-collapse', function(e) {
            e.preventDefault();
            $(this).toggleClass('active');
        });

        // Сброс при изменении размера экрана
        $(window).resize(function() {
            if ($(this).width() > 768) {
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                    $('.js-menu-toggle').removeClass('active');
                }
            }
        });

        // Клик вне меню для закрытия
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
    // 2. Слайдеры и Плагины (с безопасной проверкой наличия)
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

    // Анимация появления элементов
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

        copyToClipboard(linkToCopy, function() {
            $btn.text('✅ Ссылка скопирована!');
            setTimeout(function() { $btn.text(originalText); }, 3000);
        });
    });

    // -------------------------------------------------------------
    // 5. Показ Баннера (раз в сутки)
    // -------------------------------------------------------------
    var today = new Date().toISOString().slice(0, 10);
    var lastShownDate = localStorage.getItem('yandexBannerLastShown');

    if (lastShownDate !== today) {
        setTimeout(function() {
            var $banner = $('#top-yandex-banner');
            if ($banner.length) {
                $banner.removeClass('top-banner-hidden').addClass('top-banner-visible');
                localStorage.setItem('yandexBannerLastShown', today);

                var autoHideTimer = setTimeout(function() {
                    $banner.removeClass('top-banner-visible').addClass('top-banner-hidden');
                }, 7000);

                $('#closeBannerBtn').on('click', function() {
                    clearTimeout(autoHideTimer);
                    $banner.removeClass('top-banner-visible').addClass('top-banner-hidden');
                });
            }
        }, 1000);
    }

    // -------------------------------------------------------------
    // 6. Обработка Всплывающих Popover
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
            copyToClipboard(payUrl, function() {
                $btn.text('СКИЛКА СКОПИРОВАНА! ✓');
                setTimeout(function() { $btn.text(originalText); }, 2500);
            });
        }
    });

    // Вспомогательная функция копирования
    function copyToClipboard(text, successCallback) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(successCallback).catch(function() {
                prompt("Скопируйте ссылку на оплату:", text);
            });
        } else {
            prompt("Скопируйте ссылку на оплату:", text);
        }
    }
});