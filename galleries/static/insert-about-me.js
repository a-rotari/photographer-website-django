const aboutMe = document.querySelector('.about-me');
if (aboutMe) {
    const gallery = document.querySelector('.gallery');
    const galleryStyles = window.getComputedStyle(gallery);
    const numberOfColumns = galleryStyles.getPropertyValue('columns').slice(-1);
    if (numberOfColumns > 0) {
        const children = gallery.children;
        const totalNumberOfChildren = children.length;
        const elementsInOneColumn = Math.round(totalNumberOfChildren / numberOfColumns);
        // const targetElement = children[totalNumberOfPhotos - 1 - elementsInOneColumn];
        console.log('Total number of children:' + totalNumberOfChildren);
        const modulo = totalNumberOfChildren % numberOfColumns;
        // targetElement.insertAdjacentElement('afterend', aboutMe);
        // console.log('Inserted!');
        console.log('Elements in one column: ' + elementsInOneColumn);
        console.log('Leftover elements: ' + modulo);
    } else {
        console.log('Something!');
    }
}
