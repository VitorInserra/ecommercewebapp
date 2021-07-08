var scrollPerClick;
var ImagePadding = 20;
let size = window.innerWidth;

if (size >= 1200) {
    scrollPerClick = 762;
} else if (size >= 768 && size < 1200) {
    scrollPerClick = 508;
}else {
    scrollPerClick = 254;
} 

// Scroll Functionality
var scrollAmount = 0;
function sliderScrollLeft(selid) {
    const sliders = document.getElementById(selid);
    sliders.scrollTo({
        top: 0,
        left: (scrollAmount -= scrollPerClick),
        behavior: "smooth",
    });
    if (scrollAmount < 0) {
        scrollAmount = 0;
    }

    console.log("Scroll Amount: ", scrollAmount);
}

function sliderScrollRight(selid) {
    const sliders = document.getElementById(selid);
    if (scrollAmount <= sliders.scrollWidth - sliders.clientWidth) {
        sliders.scrollTo({
            top: 0,
            left: (scrollAmount += scrollPerClick),
            behavior: "smooth",
        });
    }
    console.log("Scroll Amount: ", scrollAmount);
}