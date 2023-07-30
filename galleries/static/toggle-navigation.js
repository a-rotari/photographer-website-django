const closeButton = document.getElementById("galleries-close-button");
const openButton = document.getElementById("galleries-open-button");
const navMenu = document.getElementById("galleries-items");
const switcherTitle = document.getElementById("galleries-switcher")

closeButton.addEventListener("click", function() {
  navMenu.classList.add("mobile-hidden");
  closeButton.classList.add("mobile-hidden");
  switcherTitle.classList.remove("mobile-hidden");
  openButton.classList.remove("mobile-hidden");
});

openButton.addEventListener("click", function() {
  openButton.classList.add("mobile-hidden");
  switcherTitle.classList.add("mobile-hidden");
  closeButton.classList.remove("mobile-hidden");
  navMenu.classList.remove("mobile-hidden");
});
