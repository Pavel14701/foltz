document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.need-background-image');
    elements.forEach(element => {
        const imageName = element.getAttribute('data-image-name');
        const dataBackgroundImgPos = element.getAttribute('data-image-back-pos');

        fetch(`/get-image-url/${imageName}/`)
            .then(response => response.json())
            .then(data => {
                element.style.backgroundImage = `url(${data.image_url})`;
                element.style.backgroundSize = 'contain';
                element.style.backgroundRepeat = 'no-repeat';
                if (dataBackgroundImgPos) {
                    element.style.backgroundPosition = dataBackgroundImgPos.trim();
                } else {
                    element.style.backgroundPosition = 'center';
                }
            })
            .catch(error => console.error('Error fetching image:', error));
    });
});
