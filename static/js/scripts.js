// Tablas dinámicas
$(document).ready(function() {
    $('#dynamicTable').DataTable({
        pagingType: 'simple_numbers' // Opciones: 'numbers', 'simple', 'simple_numbers', 'full', 'full_numbers'
    });
});
// Para el buscador en select
$(document).ready(function() {
    $('.select2').select2();
});

// Para el carrusel de fotos 
document.addEventListener("DOMContentLoaded", function() {
    let covers = document.querySelectorAll('.book-cover');
    let currentIndex = 0;

    function showNextCover() {
        covers[currentIndex].style.display = 'none';
        currentIndex = (currentIndex + 1) % covers.length;
        covers[currentIndex].style.display = 'block';
    }

    if (covers.length > 0) {
        covers[0].style.display = 'block';
        setInterval(showNextCover, 3000); // Cambia la imagen cada 3 segundos
    }
  });

// Para calcular el average_rating sobre 100
function calculateRating(rating) {
    return rating * 20;
}

document.addEventListener("DOMContentLoaded", function() {
    var ratingElement = document.getElementById("average-rating");
    var rating = parseFloat(ratingElement.textContent);
    var ratingOver100 = calculateRating(rating);
    document.getElementById("rating-over-100").textContent = ratingOver100;
});
