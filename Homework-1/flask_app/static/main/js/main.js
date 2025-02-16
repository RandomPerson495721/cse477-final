
// Function to toggle the visibility of the navigation menu based on the 'menu-bar' button
document.getElementById('menu-bar').addEventListener('click', function () {
    var navMenu = document.getElementById('navMenu');

    if (navMenu.classList.contains('banner-buttons')) {
        navMenu.classList.replace('banner-buttons', 'banner-buttons-expanded');
    } else {
        navMenu.classList.replace('banner-buttons-expanded', 'banner-buttons');
    }
});

// Function to reset the navigation menu to the default class when the window is resized
window.addEventListener('resize', function () {
    var navMenu = document.getElementById('navMenu');
    if ((window.innerWidth > 650) && (navMenu.classList.contains('banner-buttons-expanded'))) {
        navMenu.classList.replace('banner-buttons-expanded', 'banner-buttons');
    }
});