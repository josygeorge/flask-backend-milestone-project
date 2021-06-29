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

    /* ----- Remove icon is shown, if no. of input textbox are more than 1 ----- */
    // Edit definition --
    if($('#edit_word_definition input.definition').length > 1) {
        $('<div id="remove-definition-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-definition-textbox');
    }
    // Edit synonym --
    if($('#edit_word_definition input.synonym').length > 1) {
        $('<div id="remove-synonym-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-synonym-textbox');
    }
    // Edit antonym --
    if($('#edit_word_definition input.antonym').length > 1) {
        $('<div id="remove-antonym-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-antonym-textbox');
    }

    /* -----------------------------------
    Add Word Definitions Array of textbox 
    ------------------------------------ */
    $('#add-definition-textbox').on('click', function (e) {
        e.preventDefault();
        // remove the multi occurence of remove on each add definition
        $(document).find('#remove-definition-textbox').remove();

        $('<input type="text"/>')
            .addClass('form-control mt-2 definition required')
            .attr('name', 'definitions[]')
            .attr('id', 'definitions')
            .attr('required', true)
            .attr('placeholder', 'Other definition')
            .insertBefore(this);
        $('<div id="remove-definition-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-definition-textbox');
            
    });
    // Remove Word Definitions Array of textbox excluding 1st input:textbox
    $(document).on("click", '#remove-definition-textbox', function () {
        if($('input.definition').length > 1) {
            $("div.definitions").find("input:last").remove();
        }
        // On DOMSubtreeModified remove the icon if the input textbox is at first
        $('body').on('DOMSubtreeModified', 'div.definitions', function(){
            if($('input.definition').length < 2) {
                $(document).find('#remove-definition-textbox').remove();
            }
        });
            
    });
    /* --------------------------
    Add Synonyms Array of textbox 
    ----------------------------- */
    $('#add-synonym-textbox').on('click', function (e) {
        e.preventDefault();
        // remove the multi occurence of remove on each add synonym
        $(document).find('#remove-synonym-textbox').remove();
        $('<input type="text"/>')
            .addClass('form-control mt-2 synonym')
            .attr('name', 'synonyms[]')
            .attr('id', 'synonyms')
            .attr('required', true)
            .attr('placeholder', 'Other synonym')
            .insertBefore(this);
        $('<div id="remove-synonym-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-synonym-textbox');
    });
    // Remove Synonyms Array of textbox excluding 1st input:textbox
    $(document).on("click", '#remove-synonym-textbox', function () {
        if($('input.synonym').length > 1) {
            $("div.synonyms").find("input:last").remove();
        }
        // On DOMSubtreeModified remove the icon if the input textbox is at first
        $('body').on('DOMSubtreeModified', 'div.synonyms', function(){
            if($('input.synonym').length < 2) {
                $(document).find('#remove-synonym-textbox').remove();
            }
        });
    });

    /* ---------------------------
    Add Antonyms Array of textbox 
    ---------------------------- */
    $('#add-antonym-textbox').on('click', function (e) {
        e.preventDefault();
        // remove the multi occurence of remove on each add antonym
        $(document).find('#remove-antonym-textbox').remove();

        $('<input type="text"/>')
            .addClass('form-control mt-2 antonym required')
            .attr('name', 'antonyms[]')
            .attr('id', 'antonyms')
            .attr('required', true)
            .attr('placeholder', 'Other antonym')
            .insertBefore(this);
        $('<div id="remove-antonym-textbox" class="text-right hover-me">Remove&nbsp;<i class="fas fa-minus-square"></i></div>')
            .insertAfter('#add-antonym-textbox');
    });
    // Remove Antonyms Array of textbox excluding 1st input:textbox
    $(document).on("click", '#remove-antonym-textbox', function () {
        if($('input.antonym').length > 1) {
            $("div.antonyms").find("input:last").remove();
        }
        // On DOMSubtreeModified remove the icon if the input textbox is at first
        $('body').on('DOMSubtreeModified', 'div.antonyms', function(){
            if($('input.antonym').length < 2) {
                $(document).find('#remove-antonym-textbox').remove();
            }
        });
        // $(document).bind('DOMSubtreeModified', function () {
        //     if($('input.antonym').length < 2) {
        //         $(document).find('#remove-antonym-textbox').remove();
        //     }
        //  }); 
    });

});
