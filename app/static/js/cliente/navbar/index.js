const navToggler = document.querySelector(".nav-toggler");
navToggler.addEventListener("click", navToggle)

function navToggle() {
   navToggler.classList.toggle("active");
   const nav = document.querySelector(".nav");
   nav.classList.toggle("open");
   if(nav.classList.contains("open")){
       nav.style.maxHeight = nav.scrollHeight + "px"
   }
   else{
       nav.removeAttribute("style");
   }
}

function myFunction() {
    var x = document.getElementById("mydropDown");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}