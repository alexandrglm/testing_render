document.addEventListener("DOMContentLoaded", function () {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");

    burger.addEventListener("click", function (event) {
        event.stopPropagation();
        nav.classList.toggle("nav-active");
        if (nav.classList.contains("nav-active")) {
            nav.style.display = "flex";
        } else {
            nav.style.display = "none";
        }
    });

    function navbarResize() {
        if (window.innerWidth > 768) {
            nav.classList.remove("nav-active");
            nav.style.display = "flex"; 
        } else {
            nav.style.display = "none";
        }
    }
    window.addEventListener("resize", navbarResize);
    navbarResize();


    document.addEventListener("click", function (event) {
        if (
            !event.target.closest(".burger") &&
            !event.target.closest(".nav-links") &&
            !event.target.closest(".site-title")
        ) {
            nav.classList.remove("nav-active");
            nav.style.display = "none";
        }
    });
});