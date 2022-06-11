var stars = document.querySelectorAll(".star-icon");
var myFunction = function (e) {
  var classStar = e.target.classList;
  if (!classStar.contains("ativo")) {
    stars.forEach(function (star) {
      star.classList.remove("ativo");
    });
    classStar.add("ativo");

    var numberStars = e.target.getAttribute("data-avaliacao");
    document.getElementById("number-star").value = numberStars;

  }
};

for (var i = 0; i < stars.length; i++) {
  stars[i].addEventListener("click", myFunction);
  document.getElementById("number-star").value = 1;
}
