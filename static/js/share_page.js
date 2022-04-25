function hideToggle(head_element) {
    let pl_content = head_element.parentElement.children[1]
    console.log(pl_content.style.display)
    if (pl_content.style.display === "none" || pl_content.style.display == "") {
        pl_content.style.display = "block"
    }
    else {
        pl_content.style.display = "none"
    }
}