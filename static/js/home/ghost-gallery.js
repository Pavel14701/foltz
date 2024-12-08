/**
 * @type {number}
 */
let currentIndex = 0;
/**
 * @type {number|undefined}
 */
let interval;
/**
 * @type {number}
 */
let remainingTime = 7000;
/**
 * @type {number}
 */
let startTime;

/**
 * @param {NodeListOf<Element>} cards
 */
function showNextCard(cards) {
    const oldLoader = cards[currentIndex].querySelector('.change-loader');
    oldLoader.classList.remove('restart-animation');

    cards[currentIndex].classList.remove('setted');
    currentIndex = (currentIndex + 1) % cards.length;
    cards[currentIndex].classList.add('setted');

    const newLoader = cards[currentIndex].querySelector('.change-loader');
    void newLoader.offsetWidth;
    newLoader.classList.add('restart-animation');

    remainingTime = 7000;
    startInterval(cards);
}

/**
 * @param {NodeListOf<Element>} cards
 */
function startInterval(cards) {
    startTime = Date.now();
    interval = setTimeout(() => showNextCard(cards), remainingTime);
}

function stopInterval() {
    clearTimeout(interval);
    remainingTime -= Date.now() - startTime;
}

document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.gallery-wrapper .card-wrapper');
    const initialLoader = cards[currentIndex].querySelector('.change-loader');
    initialLoader.classList.add('restart-animation');
    cards[currentIndex].classList.add('setted');
    startInterval(cards);

    cards.forEach(cardWrapper => {
        const card = cardWrapper.querySelector('.card');
        const loader = card.querySelector('.change-loader');

        card.addEventListener('mouseenter', stopInterval);
        card.addEventListener('mouseleave', () => startInterval(cards));
    });
});
