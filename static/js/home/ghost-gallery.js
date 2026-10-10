document.addEventListener('DOMContentLoaded', () => {

    // Единая константа: должна совпадать с animation: loading 7s в gallery.css.
    const SLIDE_TIME = 7000;

    const galleries = document.querySelectorAll('.gallery-wrapper');

    galleries.forEach(gallery => {
        let currentIndex = 0;
        let timer = null;
        let remainingTime = SLIDE_TIME;
        let startTime = 0;

        const cards = gallery.querySelectorAll('.card-wrapper');

// sourcery skip: avoid-function-declarations-in-blocks
        function showNextCard() {
            timer = null;

            const oldLoader = cards[currentIndex].querySelector('.change-loader');
            oldLoader.classList.remove('restart-animation');

            cards[currentIndex].classList.remove('setted');
            currentIndex = (currentIndex + 1) % cards.length;
            cards[currentIndex].classList.add('setted');

            const newLoader = cards[currentIndex].querySelector('.change-loader');
            void newLoader.offsetWidth; // reflow — перезапуск анимации ползунка
            newLoader.classList.add('restart-animation');

            remainingTime = SLIDE_TIME;
            startInterval();
        }

        function startInterval() {
            // Раньше mouseleave + IntersectionObserver могли навесить несколько
            // параллельных таймеров — карточка менялась раньше ползунка.
            if (timer) return;
            if (remainingTime <= 0) remainingTime = SLIDE_TIME;
            startTime = Date.now();
            timer = setTimeout(() => showNextCard(), remainingTime);
        }

        function stopInterval() {
            if (!timer) return;
            clearTimeout(timer);
            timer = null;
            // Остаток не уходит в минус: отрицательное значение давало
            // мгновенную смену сразу после ухода курсора.
            remainingTime = Math.max(remainingTime - (Date.now() - startTime), 0);
        }

        const initialLoader = cards[currentIndex].querySelector('.change-loader');
        initialLoader.classList.add('restart-animation');
        cards[currentIndex].classList.add('setted');
        startInterval();

        cards.forEach(cardWrapper => {
            const card = cardWrapper.querySelector('.card');

            card.addEventListener('mouseenter', stopInterval);
            card.addEventListener('mouseleave', startInterval);
        });

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startInterval();
                } else {
                    stopInterval();
                }
            });
        });

        observer.observe(gallery);
    });
});
