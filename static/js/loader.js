function setCustomDisplay(selector) {
    let element = document.querySelector(selector);
    let customDisplay = element.getAttribute('data-display');
    element.style.display = customDisplay;
}

window.addEventListener('load', function() {
    setTimeout(function() {
        document.body.classList.remove('loading');
        document.documentElement.classList.remove('loading');
        document.body.classList.add('loaded');
        document.documentElement.classList.add('loaded');
        document.getElementById('loading').style.display = 'none';
        setCustomDisplay('.content');
        document.body.style.overflow = 'auto';
    }, 2000);
});

document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('loading');
    document.documentElement.classList.add('loading');
    let links = document.querySelectorAll('a');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            document.getElementById('loading').style.display = 'flex';
            document.querySelector('.content').style.display = 'none';
        });
    });
});










