window.addEventListener("load", (event) => {
    let toggleNavButton = window.document.getElementById("toggle-navbar");
    let navBar = window.document.getElementById("navbar");
    toggleNavButton.addEventListener("click", function(e) {
        console.log(navBar.style);
        navBar.classList.toggle("visible");
    })
});