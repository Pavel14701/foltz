/* Слайдер отзывов: автопрокрутка 10с, пауза при ховере/фокусе, стрелки, точки, свайп. */
(function () {
    'use strict';
    var AUTOPLAY_DELAY = 10000;

    function init() {
        document.querySelectorAll('[data-reviews-slider]').forEach(initSlider);
    }

    function initSlider(slider) {
        var viewport = slider.querySelector('.reviews-slider__viewport');
        var track = slider.querySelector('.reviews-slider__track');
        if (!viewport || !track || !track.children.length) {
            return;
        }
        var prevBtn = slider.querySelector('.reviews-slider__btn--prev');
        var nextBtn = slider.querySelector('.reviews-slider__btn--next');
        var dotsBox = slider.querySelector('.reviews-slider__dots');
        var dots = [];
        var idx = 0;
        var timer = null;

        function metrics() {
            var card = track.children[0];
            var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
            var step = card.getBoundingClientRect().width + gap;
            var perView = Math.max(1, Math.round(viewport.clientWidth / step));
            return { step: step, maxIdx: Math.max(0, track.children.length - perView) };
        }

        function go(i) {
            var m = metrics();
            idx = ((i % (m.maxIdx + 1)) + m.maxIdx + 1) % (m.maxIdx + 1); /* цикл в обе стороны */
            track.style.transform = 'translateX(-' + (idx * m.step) + 'px)';
            syncDots(m.maxIdx);
            if (prevBtn) prevBtn.classList.toggle('is-hidden', m.maxIdx === 0);
            if (nextBtn) nextBtn.classList.toggle('is-hidden', m.maxIdx === 0);
        }

        function syncDots(expectedCount) {
            if (!dotsBox) {
                return;
            }
            if (dots.length !== expectedCount) {
                dotsBox.innerHTML = '';
                dots = [];
                for (var k = 0; k < expectedCount; k++) {
                    var d = document.createElement('button');
                    d.type = 'button';
                    d.className = 'blog-gallery__dot' + (k === 0 ? ' is-active' : '');
                    d.setAttribute('aria-label', 'Отзывы, слайд ' + (k + 1));
                    (function (k) { d.addEventListener('click', function () { go(k); }); })(k);
                    dotsBox.appendChild(d);
                    dots.push(d);
                }
            }
            dots.forEach(function (d, k) { d.classList.toggle('is-active', k === idx); });
        }

        function startAutoplay() {
            stopAutoplay();
            timer = setInterval(function () { go(idx + 1); }, AUTOPLAY_DELAY);
        }

        function stopAutoplay() {
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
        }

        if (prevBtn) prevBtn.addEventListener('click', function () { go(idx - 1); });
        if (nextBtn) nextBtn.addEventListener('click', function () { go(idx + 1); });

        /* пауза автопрокрутки при ховере и фокусе с клавиатуры */
        slider.addEventListener('mouseenter', stopAutoplay);
        slider.addEventListener('mouseleave', startAutoplay);
        slider.addEventListener('focusin', stopAutoplay);
        slider.addEventListener('focusout', startAutoplay);

        /* свайп на тач-экранах */
        var startX = null;
        slider.addEventListener('touchstart', function (e) {
            startX = e.touches[0].clientX;
            stopAutoplay();
        }, { passive: true });
        slider.addEventListener('touchend', function (e) {
            if (startX !== null) {
                var dx = e.changedTouches[0].clientX - startX;
                if (dx > 40) go(idx - 1);
                if (dx < -40) go(idx + 1);
                startX = null;
            }
            startAutoplay();
        }, { passive: true });

        window.addEventListener('resize', function () { go(idx); });

        go(0);
        startAutoplay();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
