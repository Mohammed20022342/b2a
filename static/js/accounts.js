document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const nav = document.querySelector("nav");

    hamburger.addEventListener("click", () => {
        nav.classList.toggle("open");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const searchIcon = document.querySelector(".search-icon");
    const searchBar = document.querySelector(".search-bar");

    // Toggle search bar visibility for small screens
    searchIcon.addEventListener("click", () => {
        searchBar.classList.toggle("open");
        searchBar.classList.toggle("show"); // Ensure the transition works
    });
});
