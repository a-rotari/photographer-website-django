// replace the placeholder with actual image links
const lazyLoad = (picture) => {
    const img = picture.querySelector('img');
    const sources = picture.querySelectorAll('source');

    sources.forEach((source) => {
        source.srcset = source.dataset.srcset;
        source.removeAttribute('data-srcset');
    });
    img.src = img.dataset.src;
    img.removeAttribute('data-src');
}

// initialize the intersection observer
const imgObserver = new IntersectionObserver((entries, self) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            lazyLoad(entry.target);
            self.unobserve(entry.target);
        }
    });
});

// make the observer start observing the picture elements
document.querySelectorAll('.gallery__photo').forEach((picture) => {
    imgObserver.observe(picture);
});