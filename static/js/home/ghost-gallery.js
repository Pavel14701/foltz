document.addEventListener('DOMContentLoaded', () => {

    const galleries = document.querySelectorAll('.gallery-wrapper');
    
    galleries.forEach(gallery => {
        let currentIndex = 0;
        let interval;
        let remainingTime = 7000;
        let startTime;

        const cards = gallery.querySelectorAll('.card-wrapper');

        function showNextCard() {
            const oldLoader = cards[currentIndex].querySelector('.change-loader');
            oldLoader.classList.remove('restart-animation');

            cards[currentIndex].classList.remove('setted');
            currentIndex = (currentIndex + 1) % cards.length;
            cards[currentIndex].classList.add('setted');

            const newLoader = cards[currentIndex].querySelector('.change-loader');
            void newLoader.offsetWidth;
            newLoader.classList.add('restart-animation');

            remainingTime = 7000;
            startInterval();
        }

        function startInterval() {
            startTime = Date.now();
            interval = setTimeout(() => showNextCard(), remainingTime);
        }

        function stopInterval() {
            clearTimeout(interval);
            remainingTime -= Date.now() - startTime;
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
