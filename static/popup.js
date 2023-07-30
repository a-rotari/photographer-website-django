// add click event listener to image container to hide the popup
let photoPopups = document.getElementsByClassName('photo-popup');
for (let i = 0; i < photoPopups.length; i++) {
    photoPopups[i].addEventListener('click', function() {
        this.classList.remove('photo-popup--visible');
    });
}

// add click event listener to the image to trigger the popup
let galleryPhotos = document.getElementsByClassName('gallery__photo');
for (let i = 0; i < galleryPhotos.length; i++) {
    galleryPhotos[i].addEventListener('click', function () {
        this.nextElementSibling.classList.add('photo-popup--visible');
    });
}