 AOS.init({
 	duration: 800,
 	easing: 'slide',
 	once: true
 });

jQuery(document).ready(function($) {

	"use strict";

	

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

    $('body').on('click', '.js-menu-toggle, .site-mobile-menu-close', function(e) {
        e.preventDefault();
        if ($('body').hasClass('offcanvas-menu')) {
            $('body').removeClass('offcanvas-menu');
        }
    });

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();


	var sitePlusMinus = function() {
		$('.js-btn-minus').on('click', function(e){
			e.preventDefault();
			if ( $(this).closest('.input-group').find('.form-control').val() != 0  ) {
				$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) - 1);
			} else {
				$(this).closest('.input-group').find('.form-control').val(parseInt(0));
			}
		});
		$('.js-btn-plus').on('click', function(e){
			e.preventDefault();
			$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) + 1);
		});
	};
	// sitePlusMinus();


	var siteSliderRange = function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
	};
	// siteSliderRange();


	
	var siteCarousel = function () {
		if ( $('.nonloop-block-13').length > 0 ) {
			$('.nonloop-block-13').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 0,
		    autoplay: true,
		    nav: true,
				navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
		    responsive:{
	        600:{
	        	margin: 0,
	        	nav: true,
	          items: 2
	        },
	        1000:{
	        	margin: 0,
	        	stagePadding: 0,
	        	nav: true,
	          items: 3
	        },
	        1200:{
	        	margin: 0,
	        	stagePadding: 0,
	        	nav: true,
	          items: 4
	        }
		    }
			});
		}


		if ( $('.nonloop-block-14').length > 0 ) {
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
		    responsive:{
	        600:{
	        	margin: 20,
	        	nav: true,
	          items: 2
	        },
	        1000:{
	        	margin: 30,
	        	
	        	nav: true,
	          items: 2
	        },
	        1200:{
	        	margin: 30,
	        	
	        	nav: true,
	          items: 3
	        }
		    }
			});
		}

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
	};
	siteCarousel();

	var siteStellar = function() {
		$(window).stellar({
	    responsive: false,
	    parallaxBackgrounds: true,
	    parallaxElements: true,
	    horizontalScrolling: false,
	    hideDistantElements: false,
	    scrollProperty: 'scroll'
	  });
	};
	siteStellar();

	var siteCountDown = function() {

		$('#date-countdown').countdown('2020/10/10', function(event) {
		  var $this = $(this).html(event.strftime(''
		    + '<span class="countdown-block"><span class="label">%w</span> weeks </span>'
		    + '<span class="countdown-block"><span class="label">%d</span> days </span>'
		    + '<span class="countdown-block"><span class="label">%H</span> hr </span>'
		    + '<span class="countdown-block"><span class="label">%M</span> min </span>'
		    + '<span class="countdown-block"><span class="label">%S</span> sec</span>'));
		});
				
	};
	siteCountDown();

	var siteDatePicker = function() {

		if ( $('.datepicker').length > 0 ) {
			$('.datepicker').datepicker();
		}

	};
	siteDatePicker();

	var siteSticky = function() {
		$(".js-sticky-header").sticky({topSpacing:0});
	};
	siteSticky();

	// navigation
    var OnePageNavigation = function() {
        var navToggler = $('.site-menu-toggle');

        $("body").on("click", ".main-menu li a, .smoothscroll, .site-mobile-menu .site-nav-wrap li a", function(e) {
            var href = $(this).attr('href');

            // Если это якорная ссылка (начинается с # и не состоит из одного #)
            if (href && href.startsWith('#') && href !== '#') {
                e.preventDefault();

                var target = $(href);
                if (target.length) {
                    $('html, body').animate({
                        'scrollTop': target.offset().top
                    }, 600, 'easeInOutCirc', function(){
                        window.location.hash = href;
                    });
                }

                // Закрываем мобильное меню после клика по якорю
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
                }
            }
            // Если это обычная ссылка (переход на другую страницу),
            // e.preventDefault() НЕ вызываем — браузер спокойно перейдет по URL!
            else if (href && href !== '#') {
                // Закрываем меню для плавности перед переходом
                if ($('body').hasClass('offcanvas-menu')) {
                    $('body').removeClass('offcanvas-menu');
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

  	}) 

  };
	siteScroll();

    const items = $('.animated-item');
    items.each(function(index) {
        $(this).css('opacity', 0);
        $(this).delay(index * 200).animate({opacity: 1}, 500);
    });


});

jQuery(document).ready(function($) {

    // 1. При клике на "ВЫБРАТЬ" подставляем динамическую ссылку оплаты в кнопку модалки
    $('.btn-open-pay-modal').on('click', function() {
        var payUrl = $(this).attr('data-pay-url') || $(this).data('pay-url');
        $('#modalProceedBtn').attr('href', payUrl);
    });

    // 2. Копирование именно этой ссылки из href кнопки модального окна
    $('#modalCopyBtn').on('click', function(e) {
        e.preventDefault();
        var linkToCopy = $('#modalProceedBtn').attr('href');

        if (!linkToCopy || linkToCopy === '#') {
            alert('Ссылка не найдена!');
            return;
        }

        var $btn = $(this);
        var originalText = $btn.text();

        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(linkToCopy).then(function() {
                $btn.text('✅ Ссылка скопирована!');
                setTimeout(function() {
                    $btn.text(originalText);
                }, 3000);
            }).catch(function() {
                fallbackCopyText(linkToCopy, $btn, originalText);
            });
        } else {
            fallbackCopyText(linkToCopy, $btn, originalText);
        }
    });

    function fallbackCopyText(text, $btn, originalText) {
        prompt("Скопируйте ссылку на оплату:", text);
    }

});


// Проверка: показывали ли уже плашку сегодня?
var today = new Date().toISOString().slice(0, 10); // Формат: "2026-08-15"
var lastShownDate = localStorage.getItem('yandexBannerLastShown');

if (lastShownDate !== today) {
    // Если сегодня еще НЕ показывали — запускаем анимацию через 1 секунду
    setTimeout(function() {
        var $banner = $('#top-yandex-banner');

        // 1. Показываем плашку
        $banner.removeClass('top-banner-hidden').addClass('top-banner-visible');

        // 2. Сохраняем сегодняшнюю дату в память браузера
        localStorage.setItem('yandexBannerLastShown', today);

        // 3. Автоматически скрываем плашку через 7 секунд
        var autoHideTimer = setTimeout(function() {
            $banner.removeClass('top-banner-visible').addClass('top-banner-hidden');
        }, 7000);

        // 4. Закрытие по крестику
        $('#closeBannerBtn').on('click', function() {
            clearTimeout(autoHideTimer);
            $banner.removeClass('top-banner-visible').addClass('top-banner-hidden');
        });

    }, 1000);
}