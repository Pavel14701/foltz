(function () {
    var HIDE_DELAY = 600;  // задержка после готовности DOM
    var FORCE_HIDE = 2500; // страховка: прелоадер не может жить дольше
    var resetTimer = null;

    function showPageContent() {
        // Элементы с data-display показываем заданным в атрибуте способом
        document.querySelectorAll('[data-display]').forEach(function (element) {
            element.style.display = element.getAttribute('data-display');
        });
        var wrapper = document.querySelector('.content-wrapper');
        if (wrapper) {
            wrapper.style.display = '';
        }
    }

    function hidePreloader() {
        document.body.classList.remove('loading');
        document.documentElement.classList.remove('loading');
        document.body.classList.add('loaded');
        var preloader = document.getElementById('loading');
        if (preloader) {
            preloader.style.display = 'none';
        }
        showPageContent();
        document.body.style.overflow = '';
    }

    // Ждём только DOM, а не window.load: картинки и шрифты подгружаются фоном,
    // зависший ресурс больше не блокирует страницу (было: load + 2 секунды).
    function scheduleHide() {
        setTimeout(hidePreloader, HIDE_DELAY);
        setTimeout(hidePreloader, FORCE_HIDE); // самосброс при любых обстоятельствах
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', scheduleHide);
    } else {
        scheduleHide();
    }

    // Индикатор при переходе между страницами: показываем прелоадер,
    // но с самосбросом — если навигация не случилась, страницу возвращаем.
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('a[href]').forEach(function (link) {
            var href = link.getAttribute('href') || '';
            if (href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) {
                return;
            }
            link.addEventListener('click', function (event) {
                // модификаторы/средняя кнопка — откроется в новой вкладке, не прячем страницу
                if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) {
                    return;
                }
                var preloader = document.getElementById('loading');
                if (preloader) {
                    preloader.style.display = 'flex';
                }
                clearTimeout(resetTimer);
                resetTimer = setTimeout(hidePreloader, 4000);
            });
        });
    });
})();
