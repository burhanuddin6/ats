// Get the modal
document.addEventListener('DOMContentLoaded', function() {
  var modal = document.getElementById("modal");
  
  // Get the button that opens the modal
  var btn = document.getElementById("email-candidate");
  
  // Get the <span> element that closes the modal
  var span = document.getElementById("modal-close");
  
  // When the user clicks the button, open the modal 
  btn.onclick = function() {
    modal.style.display = "block";
  }
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }
});