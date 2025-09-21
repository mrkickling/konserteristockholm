const headers = document.querySelectorAll('.concert-date-header');
let currentActiveHeader = headers[0]; // Start with the first header
const firstHeaderTop = headers[0].offsetTop;

// Listen to the scroll event
window.addEventListener('scroll', () => {
    let scrollPosition = window.scrollY;

    if (currentActiveHeader && scrollPosition < firstHeaderTop) {
        currentActiveHeader.classList.remove('active');
        currentActiveHeader = null;
    }

    headers.forEach(header => {
        // Get the distance of the header from the top of the page
        const headerTop = header.offsetTop;

        // If the header has scrolled past the top of the window
        if (scrollPosition >= headerTop) {
            // Remove the active class from the current active header
            if (currentActiveHeader) {
                currentActiveHeader.classList.remove('active');
            }

            // Set the new header as active
            currentActiveHeader = header;
            currentActiveHeader.classList.add('active');
        }

    });
});