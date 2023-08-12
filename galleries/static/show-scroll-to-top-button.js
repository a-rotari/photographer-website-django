const scrollButton = document.querySelector('.scroll-to-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 2000) {
        scrollButton.classList.add('show');
    } else {
        scrollButton.classList.remove('show');
    }
});

scrollButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
