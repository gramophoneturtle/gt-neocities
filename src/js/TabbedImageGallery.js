/** https://www.w3schools.com/howto/howto_js_tab_img_gallery.asp */

function expandArtWork(imgs) {
    var expandImg = document.getElementById("expandedImg");
    expandImg.src = imgs.src;
    expandImg.alt = imgs.alt;
    expandImg.parentElement.style.display = "block";
}