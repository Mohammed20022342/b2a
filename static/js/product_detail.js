function changeMainImage(newImageUrl) {
    const mainImage = document.getElementById('main-image');
    if (mainImage) {
        mainImage.src = newImageUrl; // Update the main image source
    }
}
