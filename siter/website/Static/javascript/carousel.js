const sliders,;
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
    sliders= document.querySelector("selid")
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
    sliders = document.querySelector("selid")
    if (scrollAmount <= sliders.scrollWidth - sliders.clientWidth) {
        sliders.scrollTo({
            top: 0,
            left: (scrollAmount += scrollPerClick),
            behavior: "smooth",
        });
    }
    console.log("Scroll Amount: ", scrollAmount);
}