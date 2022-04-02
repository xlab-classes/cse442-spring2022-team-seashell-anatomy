const toggle_upvote = (song_id, button) => {
    const xhttp = new XMLHttpRequest();

    xhttp.open("POST", "toggle_upvote");
    xhttp.setRequestHeader("Content-type", "application/json");
    let song_data = {'song_id': song_id}

    // change button and request content based on button color
    if (button.style.color == "white") {
        song_data['content'] = 'downvote';
        xhttp.addEventListener('load', () => button.style.color = "");
    } else {
        song_data['content'] = 'upvote';
        xhttp.addEventListener('load', () => button.style.color = "white");
    }

    xhttp.send(JSON.stringify(song_data));
    console.log(xhttp.status);
}

const songs = document.getElementsByClassName("song-row song");
for (let song of songs) {
    const song_id = song.getAttribute("song_id");
    const button = song.getElementsByClassName("like")[0];
    console.log(button);
    button.addEventListener('click', () => toggle_upvote(song_id, button));
}
