document.addEventListener("DOMContentLoaded", () => {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");

    burger.addEventListener("click", (event) => {
        event.stopPropagation();
        nav.classList.toggle("nav-active");
        nav.style.display = nav.classList.contains("nav-active") ? "flex" : "none";
    });

    const navbarResize = () => {
        nav.style.display = window.innerWidth > 768 ? "flex" : "none";
        nav.classList.remove("nav-active");
    };

    window.addEventListener("resize", navbarResize);
    
    
    navbarResize(); 
    
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".burger, .nav-links, .site-title")) {
            nav.classList.remove("nav-active");
            nav.style.display = "none";
        }
    });
});