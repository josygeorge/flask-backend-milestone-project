$(document).ready(function(){

    // Form Validation
    // Get the forms we want to add validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // set interval for flash messages
    $("#flashes").delay(4000).slideUp(300);

    // checking the value for whether change password
    $(".new_password").css({"background": "#343a40"});
    $('.change_password').click(function() {
        // this will contain a reference to the checkbox   
        if (this.checked) {
            $(".new_password").removeAttr("disabled");
            $(".new_password").css({"background": "#f8f9fa"});
        } else {
            $(".new_password").attr("disabled", "disabled"); 
            $(".new_password").css({"background": "#343a40"});
        }
    });
});
