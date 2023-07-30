const togglePositionButton = document.getElementById("toggle-position");

togglePositionButton.addEventListener("click", function() {
    const toggledButtons = document.querySelectorAll("form.gallery__photo-move");

    for (let i = 0; i < toggledButtons.length; i++) {
        toggledButtons[i].classList.toggle("hidden");
    }
});