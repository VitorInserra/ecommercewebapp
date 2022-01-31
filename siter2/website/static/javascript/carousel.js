var scrollPerClick;
var ImagePadding = 20;

// Scroll Functionality
function sliderScrollLeft(selid) {
    if (window.innerWidth >= 1200) {
        scrollPerClick = 762;
    } else if (window.innerWidth >= 768 && window.innerWidth < 1200) {
        scrollPerClick = 508;
    } else {
        scrollPerClick = 254;
    } 

    const sliders = document.getElementById(selid);
    sliders.scrollBy({
        top: 0,
        left: -scrollPerClick,
        behavior: "smooth",
    });

    //console.log("Scroll Amount: ", scrollAmount);
}

function sliderScrollRight(selid) {
    if (window.innerWidth >= 1200) {
        scrollPerClick = 762;
    } else if (window.innerWidth >= 768 && window.innerWidth < 1200) {
        scrollPerClick = 508;
    } else {
        scrollPerClick = 254;
    } 

    const sliders = document.getElementById(selid);
    sliders.scrollBy({
        top: 0,
        left: +scrollPerClick,
        behavior: "smooth",
    })
    //console.log("Scroll Amount: ", scrollAmount);
}