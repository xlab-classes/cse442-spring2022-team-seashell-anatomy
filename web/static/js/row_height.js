let small = document.getElementById('small-button');
let large = document.getElementById('large-button');

function toLarge() {
    document.body.classList.remove("small")
    large.classList.add("selected")
    small.classList.remove("selected")
}

function toSmall() {
    document.body.classList.add("small")
    large.classList.remove("selected")
    small.classList.add("selected")
}
