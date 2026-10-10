/* Мобильное меню: бургер, закрытие по клику вне/Escape/переходу. */
(function () {
    'use strict';

    var burger = document.querySelector('.burger');
    var nav = document.getElementById('site-nav');
    if (!burger || !nav) {
        return;
    }

    function setOpen(open) {
        nav.classList.toggle('is-open', open);
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    }

    burger.addEventListener('click', function () {
        setOpen(!nav.classList.contains('is-open'));
    });

    // Закрываем меню при переходе по ссылке
    nav.addEventListener('click', function (event) {
        if (event.target.closest('a')) {
            setOpen(false);
        }
    });

    // Клик вне панели закрывает меню
    document.addEventListener('click', function (event) {
        if (nav.classList.contains('is-open')
            && !nav.contains(event.target)
            && !burger.contains(event.target)) {
            setOpen(false);
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            setOpen(false);
        }
    });

    // При возврате на десктоп панель всегда открыта по CSS, состояние сбрасываем
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) {
        if (e.matches) {
            setOpen(false);
        }
    });
})();
