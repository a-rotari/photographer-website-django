const pictures = window.document.querySelectorAll('.gallery__photo');

const config = {
    rootMargin: '50px 0px',
    threshold: 0.1
};

let imgObserver;

// replace the placeholder with actual image links
let lazyLoad = (picture) => {
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
imgObserver = new IntersectionObserver((entries, self) => {
    entries.forEach(entry => {
        if (entry.intersectionRatio > 0) {
            lazyLoad(entry.target);
            self.unobserve(entry.target);
        }
    });
}, config);

// make the observer start observing the picture elements
pictures.forEach((picture) => {
    imgObserver.observe(picture);
});
