var modal = document.getElementById('id01');
var modal2 = document.getElementById('id02');

// table booking delete modal
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// table booking edit modal
window.onclick = function(event) {
  if (event.target == modal) {
    modal2.style.display = "none";
  }
}

// search bookings in staff panel
$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

console.log('hello world');