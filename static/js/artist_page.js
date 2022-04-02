let blocker = document.getElementsByClassName("background_block");
let overlay = document.getElementsByClassName("artist_overlay");

function getArtistPage() {
    blocker.style.display = "block";
    overlay.style.display = "block";
}

function hideArtistPage() {
    overlay.style.display = "none";
    blocker.style.display = "none";
}