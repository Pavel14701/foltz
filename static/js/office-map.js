/**
 * Карта офиса на странице «О нас»: JS API Яндекс.Карт 2.1.
 * Ключ и координаты приходят из data-атрибутов контейнера (#office-map),
 * ч/б вид делает CSS-фильтр grayscale на контейнере (см. content.css).
 */
(function () {
    'use strict';

    var CONTAINER_ID = 'office-map';

    function init() {
        var el = document.getElementById(CONTAINER_ID);
        if (!el || typeof ymaps === 'undefined') {
            return;
        }

        var lat = parseFloat(el.dataset.lat);
        var lon = parseFloat(el.dataset.lon);

        var map = new ymaps.Map(el, {
            center: [lat, lon],
            zoom: 16,
            controls: ['zoomControl', 'fullscreenControl'],
        }, {
            // Без блока «Открыть в Яндекс Картах» и прочей обвязки.
            suppressMapOpenBlock: true,
            yandexMapDisablePoiInteractivity: true,
            autoFitToViewport: 'always',
        });

        // Не улетать при прокрутке страницы колесом.
        map.behaviors.disable(['scrollZoom']);

        map.geoObjects.add(new ymaps.Placemark([lat, lon], {
            hintContent: 'Фольц — офис и мастерская',
            balloonContent: 'г. Минск, ул. Сухаревская, д. 16, пом. 6',
        }, {
            preset: 'islands#redDotIcon',
        }));
    }

    if (window.ymaps && window.ymaps.ready) {
        window.ymaps.ready(init);
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            if (window.ymaps && window.ymaps.ready) {
                window.ymaps.ready(init);
            }
        });
    }
})();