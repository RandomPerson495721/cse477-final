

// Function to toggle the visibility of the navigation menu based on the 'menu-bar' button
document.getElementById('menu__bar').addEventListener('click', function (e) {
    var navMenu = document.getElementById('navMenu');

    if (navMenu.classList.contains('banner__buttons')) {
        navMenu.classList.replace('banner__buttons', 'banner__buttons--expanded');
    } else {
        navMenu.classList.replace('banner__buttons--expanded', 'banner__buttons');
    }

    e.stopPropagation();
});

// Function to reset the navigation menu to the default class when the window is resized
window.addEventListener('resize', function () {
    var navMenu = document.getElementById('navMenu');
    if ((window.innerWidth > 650) && (navMenu.classList.contains('banner__buttons--expanded'))) {
        navMenu.classList.replace('banner__buttons--expanded', 'banner__buttons');
    }
});
