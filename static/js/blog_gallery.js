/* Галереи в статьях: слайдер для 3+ фото. Подключается с defer. */
(function () {
    function init() {
        document.querySelectorAll('[data-gallery]').forEach(function (g) {
            var track = g.querySelector('.blog-gallery__track');
            if (!track) return;
            var count = track.children.length;
            var idx = 0;
            var prev = g.querySelector('.blog-gallery__btn--prev');
            var next = g.querySelector('.blog-gallery__btn--next');
            var dotsBox = g.querySelector('.blog-gallery__dots');
            var dots = [];

            for (var k = 0; k < count; k++) {
                var d = document.createElement('button');
                d.type = 'button';
                d.className = 'blog-gallery__dot' + (k === 0 ? ' is-active' : '');
                d.setAttribute('aria-label', 'Фото ' + (k + 1));
                (function (k) { d.addEventListener('click', function () { go(k); }); })(k);
                dotsBox.appendChild(d);
                dots.push(d);
            }

            function go(i) {
                idx = Math.max(0, Math.min(i, count - 1)); /* без перескока с последней на первую */
                track.style.transform = 'translateX(-' + (idx * 100) + '%)';
                dots.forEach(function (d, k) { d.classList.toggle('is-active', k === idx); });
                if (prev) prev.classList.toggle('is-disabled', idx === 0);
                if (next) next.classList.toggle('is-disabled', idx === count - 1);
            }

            if (prev) prev.addEventListener('click', function () { go(idx - 1); });
            if (next) next.addEventListener('click', function () { go(idx + 1); });
            if (prev) prev.classList.add('is-disabled'); /* стартуем с первого фото */

            /* свайп на тач-экранах */
            var startX = null;
            g.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
            g.addEventListener('touchend', function (e) {
                if (startX === null) return;
                var dx = e.changedTouches[0].clientX - startX;
                if (dx > 40) go(idx - 1);
                if (dx < -40) go(idx + 1);
                startX = null;
            }, { passive: true });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
