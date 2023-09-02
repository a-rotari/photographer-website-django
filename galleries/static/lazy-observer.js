let imgObserver;

const config = {
    rootMargin: '200px 0px 200px 0px',
    threshold: 0.1
};

initIntersectionObserver();

setTimeout(() => {
    forceLoad();
}, 300);

function isInViewport(photo) {
    const rect = photo.getBoundingClientRect();
    return (
        rect.top < (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom > 0 &&
        rect.left < (window.innerWidth || document.documentElement.clientWidth) &&
        rect.right > 0
    );
}

function forceLoad() {
    const photos = window.document.querySelectorAll('.gallery__photo');
    photos.forEach((photo) => {
        if (!photo.classList.contains('is-loaded') && isInViewport(photo)) {
            lazyLoad(photo);
        }
    });
}

function initIntersectionObserver() {
    imgObserver = new IntersectionObserver((entries, self) => {
        entries.forEach(entry => {
            if (entry.intersectionRatio > 0) {
                lazyLoad(entry.target);
                self.unobserve(entry.target);
            }
        });
    }, config);

    observeImages();
}

function observeImages() {
    const pictures = window.document.querySelectorAll('.gallery__photo');

    pictures.forEach((picture) => {
        if (!picture.classList.contains('is-loaded')) {
            imgObserver.observe(picture);
        }
    });
}


// replace the placeholder with actual image links
function lazyLoad(picture) {
    const img = picture.querySelector('img');
    const sources = picture.querySelectorAll('source');

    sources.forEach((source) => {
        source.srcset = source.dataset.srcset;
        // source.removeAttribute('data-srcset');
    });
    img.src = img.dataset.src;
    // img.removeAttribute('data-src');

    // Mark the image as loaded
    picture.classList.add('is-loaded');
}
