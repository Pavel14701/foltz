(function () {
    var input = document.querySelector('.services-search__input');
    var wrap = document.getElementById('services-grid-wrap');
    if (!input || !wrap) {
        return;
    }
    var form = input.closest('form');
    var partialUrl = form ? (form.getAttribute('data-partial-url') || '/services/') : '/services/';
    var timer = null;
    var current = null;

    function run() {
        var q = input.value.trim();
        if (q === current) {
            return;
        }
        current = q;
        var url = partialUrl + '?partial=1' + (q ? '&q=' + encodeURIComponent(q) : '');
        wrap.classList.add('is-loading');
        fetch(url, { headers: { 'X-Requested-With': 'fetch' } })
            .then(function (response) { return response.text(); })
            .then(function (html) {
                wrap.innerHTML = html;
                wrap.classList.remove('is-loading');
                if (window.history && window.history.replaceState) {
                    window.history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : window.location.pathname);
                }
            })
            .catch(function () { wrap.classList.remove('is-loading'); });
    }

    // Живой поиск: фильтруем по мере ввода, без кнопки.
    input.addEventListener('input', function () {
        clearTimeout(timer);
        timer = setTimeout(run, 250);
    });

    // Энтер/кнопка — не перезагружаем страницу, просто ищем сразу.
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            clearTimeout(timer);
            run();
        });
    }
})();
