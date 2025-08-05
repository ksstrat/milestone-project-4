document.addEventListener('DOMContentLoaded', function() {
    var myModal = new bootstrap.Modal(document.getElementById('successModal'));
    if (document.querySelector('.alert-success')) {
        myModal.show();
    }
});