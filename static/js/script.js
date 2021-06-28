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
            $(".new_password").attr("required", true);
            $(".new_password").css({"background": "#f8f9fa"});
        } else {
            $(".new_password").attr("disabled", "disabled"); 
            $(".new_password").css({"background": "#343a40"});
        }
    });
    // Add Word Definitions Array of textbox
    $('#add-definition-textbox').on('click', function (e) {
        e.preventDefault();
        $('<input type="text"/>')
            .addClass('form-control mt-2 definition required')
            .attr('name', 'definitions[]')
            .attr('id', 'definitions')
            .attr('placeholder', 'Other definition (optional)')
            .insertBefore(this);
    });
    // Add Synonyms Array of textbox
    $('#add-synonym-textbox').on('click', function (e) {
        e.preventDefault();
        $('<input type="text"/>')
            .addClass('form-control mt-2 synonym required')
            .attr('name', 'synonyms[]')
            .attr('id', 'synonyms')
            .attr('placeholder', 'Other synonym (optional)')
            .insertBefore(this);
    });
    // Add Antonyms Array of textbox
    $('#add-antonym-textbox').on('click', function (e) {
        e.preventDefault();
        $('<input type="text"/>')
            .addClass('form-control mt-2 antonym required')
            .attr('name', 'antonyms[]')
            .attr('id', 'antonyms')
            .attr('placeholder', 'Other antonym (optional)')
            .insertBefore(this);
    });
    

});
