// Show card on hover
////////////////////////////////////////////////////////

// Select all links with the class 'hover-link'
const hoverLinks = document.querySelectorAll('.hover-link');

// Function to show the image in the next sibling container
function showImage(event) {
    // Get the image URL from the data attribute
    const imageUrl = event.target.getAttribute('data-image-url');

    // Find the next sibling element (the image container)
    const targetContainer = event.target.nextElementSibling;

    // Create an image element and set its src to the image URL
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Card Image';

    // Clear the target container's content and append the new image
    targetContainer.innerHTML = '';
    targetContainer.appendChild(img);
}

// Function to hide the image when the mouse leaves the link
function hideImage(event) {
    // Find the next sibling element (the image container)
    const targetContainer = event.target.nextElementSibling;

    // Clear the image container content
    targetContainer.innerHTML = '';
}

// Because of HTMX infinite scroll, new loaded decks do not contain the event listener and will
// not show images on hover. We need to attach event listeners on each new HTMX request for more decks.

// Function to attach event listeners to hover links
function attachListeners() {
    const hoverLinks = document.querySelectorAll('.hover-link');
    hoverLinks.forEach(link => {
        link.addEventListener('mouseover', showImage);
        link.addEventListener('mouseout', hideImage);
    });
}

// HTMX afterRequest callback: called after any HTMX request is completed
document.body.addEventListener('htmx:afterRequest', function(evt) {
    attachListeners(); // Re-attach event listeners after new content is loaded
});

// Initial setup to attach event listeners to existing links
attachListeners();