let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let hideCSS = " hidden";
  let i;
  let slides = document.getElementsByClassName("slideshow-mySlides");
  let slideImages = document.getElementsByClassName("artworkShowingImage");
  let dots = document.getElementsByClassName("slideshow-demo");
  let captionText = document.getElementById("caption");
  let altText = document.getElementById("alt-text");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}

  // Hide the Prev/Next buttons if at the beginning or end
  const buttonPrev = document.getElementById('btnPrev');
  const buttonNext = document.getElementById('btnNext');

  // Hide Prev if at index 1
  if (n == 1) {
    buttonPrev.className += hideCSS;
  } else {
    buttonPrev.className = buttonPrev.className.replace(hideCSS, "");
  }

  // Hide Next if at last index
  if (n == slides.length) {
    buttonNext.className += hideCSS;
  } else {
    buttonNext.className = buttonNext.className.replace(hideCSS, "");
  }
  
  // Reset shown image - default to none
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  
  // Deactive all thumbnails
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  
  // Show the current slide and make the thumbail light up
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";

  // Update slide number
  let theSlideNumber = slideIndex + "/" + slides.length; 
  captionText.innerHTML = theSlideNumber;

  // update alt text
  altText.innerHTML="<summary>ALT</summary>" + slideImages[slideIndex-1].alt;
}