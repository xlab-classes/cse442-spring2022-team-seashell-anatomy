let blocker = document.getElementById("background_block");

let overlay = document.getElementById("artist_overlay");
let img_elem = overlay.children[0].children[0]
let name_elem = overlay.children[0].children[1]
let link_elem = overlay.children[0].children[2]
let song_list = overlay.children[1]

function getArtistPage(song_artist) {
    name_elem.innerHTML = song_artist.id;

    const xhttp = new XMLHttpRequest();
    let url = "artist?a=" + song_artist.id
    let artist_url = "https://open.spotify.com/search/" + song_artist.id;
    link_elem.setAttribute("href", artist_url);
    img_elem.setAttribute("src", "static/images/kazi_shadman.jpg");

    xhttp.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == 4) {
            let parsed = JSON.parse(this.response);
            console.log(parsed)
            for(let i = 0; i < parsed.length; i += 1) {
                song = parsed[i]
                song_list.innerHTML += "<div class=\"artist_song\"><img src=" + song['cover_url'] + "><p class=\"title\">" + song["song_name"] + "</p></td></div>"
            }
        }
    };

    xhttp.open("GET", url);
    xhttp.send();

    blocker.style.display = "block";
    overlay.style.display = "block";
}

function hideArtistPage() {
    overlay.style.display = "none";
    blocker.style.display = "none";
    song_list.innerHTML = "";
}