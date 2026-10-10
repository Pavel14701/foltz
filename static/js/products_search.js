/* Живой поиск каталога запчастей: как у услуг, но помним выбранную категорию. */
(function () {
    var input = document.querySelector('.services-search__input');
    var wrap = document.getElementById('products-grid-wrap');
    if (!input || !wrap) {
        return;
    }
    var form = input.closest('form');
    var partialUrl = form ? (form.getAttribute('data-partial-url') || '/tovary/') : '/tovary/';

    function currentCategory() {
        var match = window.location.search.match(/[?&]category=([^&]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    var timer = null;
    var current = null;

    function run() {
        var q = input.value.trim();
        var category = currentCategory();
        var key = q + '|' + category;
        if (key === current) {
            return;
        }
        current = key;
        var url = partialUrl + '?partial=1'
            + (q ? '&q=' + encodeURIComponent(q) : '')
            + (category ? '&category=' + encodeURIComponent(category) : '');
        wrap.classList.add('is-loading');
        fetch(url, { headers: { 'X-Requested-With': 'fetch' } })
            .then(function (response) { return response.text(); })
            .then(function (html) {
                wrap.innerHTML = html;
                wrap.classList.remove('is-loading');
                if (window.history && window.history.replaceState) {
                    var search = [];
                    if (q) { search.push('q=' + encodeURIComponent(q)); }
                    if (category) { search.push('category=' + encodeURIComponent(category)); }
                    window.history.replaceState(null, '', search.length ? '?' + search.join('&') : window.location.pathname);
                }
            })
            .catch(function () { wrap.classList.remove('is-loading'); });
    }

    input.addEventListener('input', function () {
        clearTimeout(timer);
        timer = setTimeout(run, 250);
    });

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            clearTimeout(timer);
            run();
        });
    }
})();
