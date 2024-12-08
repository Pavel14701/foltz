document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.need-background-image');
    elements.forEach(element => {
        const imageName = element.getAttribute('data-image-name');
        fetch(`/get-image-url/${imageName}/`)
            .then(response => response.json())
            .then(data => {
                element.style.backgroundImage = `url(${data.image_url})`;
                element.style.backgroundSize = 'contain';
                element.style.backgroundPosition = 'center'; 
                element.style.backgroundRepeat = 'no-repeat';
            })
            .catch(error => console.error('Error fetching image:', error));
    });
});