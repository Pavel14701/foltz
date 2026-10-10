document.addEventListener('DOMContentLoaded', () => {
    // Фоны карточек известны статически: ставим URL сразу, без запросов —
    // картинки грузятся параллельно и не задерживают отрисовку карточек.
    const elements = document.querySelectorAll('.need-background-image');
    elements.forEach(element => {
        const imageName = element.getAttribute('data-image-name');
        if (!imageName) {
            return;
        }
        const position = element.getAttribute('data-image-back-pos');
        element.style.backgroundImage = 'url(/static/images/' + encodeURIComponent(imageName) + ')';
        element.style.backgroundSize = 'contain';
        element.style.backgroundRepeat = 'no-repeat';
        element.style.backgroundPosition = position ? position.trim() : 'center';
    });
});
