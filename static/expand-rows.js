let photos = document.querySelectorAll('.gallery__photo');
console.log(photos.length);
console.log('it lives!')
photos.forEach(photo => {
    console.log(photo.naturalHeight);
    console.log(photo.naturalWidth);
    let photoSpan = Math.round(photo.scrollHeight / 75) + 1;
    photo.style.gridRow = `auto / span ${photoSpan}`;
    console.log(photo.style.cssText);
});