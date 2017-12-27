
$(window).load( function() {
    $('.ajax_form').submit(function(e) {
        form = $(this)
        return ajax_form_handler(e, form)
    })

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function ajax_form_handler(e, form, callback) {
        e.preventDefault();
        var alert_div = form.find(".alert")
        alert_div.removeClass("hidden")
        alert_div.removeClass("invisible")
        alert_div.addClass("alert-info")
        alert_div.html('<img class="preloader mw-100" src="/static/img/preloader.gif">Loading')
        var formData = new FormData();
        $.each($(form).find("input[type='file']"), function(i, tag) {
            $.each($(tag)[0].files, function(i, file) {
                formData.append(tag.name, file);
            });
        });
        var params = $(form).serializeArray();
        $.each(params, function (i, val) {
            console.log(i)
            console.log(val)
            formData.append(val.name, val.value);
        });
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                
                alert_div.removeClass("alert-danger")
                alert_div.removeClass("alert-info")
                alert_div.addClass("alert-success")
                if (form.attr("refresh-on-complete")) {
                    location.reload()
                } else if (form.attr("redirect-url")) {
                    location.replace(form.attr("redirect-url"))
                }
            },
            error: function(response) {
                alert_div.removeClass("alert-success")
                alert_div.removeClass("alert-info")
                alert_div.addClass("alert-danger")
            },
            complete: function(response) {
                if ("details" in response.responseJSON)
                {
                    if (response.responseJSON["details"].constructor === {}.constructor)
                    {
                        alert_div.html(JSON.stringify(response.responseJSON["details"]))
                    } else {
                        alert_div.html(response.responseJSON["details"])
                    }
                } else {
                    console.log(JSON.stringify(response.responseJSON))
                    alert_div.html(JSON.stringify(response.responseJSON))
                }
                alert_div.removeClass("hidden")
                alert_div.removeClass("invisible")

                if(form.attr('scroll-to-top')) {
                    $("html, body").animate({ scrollTop: 0 }, 500);
                }

                if ("success_url" in response.responseJSON) {
                    location.replace(response.responseJSON["success_url"])
                }

            },

        });
    }

    // get notifications count
    $.ajax({
        url: '/notification/count/',
        success: function(response) {
            var count = response['count']
            if (count > 0 )
            {
                $('.notification_count').removeClass('hidden')
                $('.notification_count').html(count)
                
            }
        }
    })

    // delete confirmation and response
    $('.delete').on('click', function(){
        redirect_url = $(this).attr('redirect-url')
        url = $(this).attr('delete-url')
        warning_msg = $(this).attr('warning-msg')
        swal({
          title: "Confirmation",
          text: warning_msg,
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Yes, delete it!'
        }).then(function () {
            $.ajax({
                type: "get",
                url: url,
                success: function(){
                    if(redirect_url) {
                        location = redirect_url
                    } else {
                        location.reload()  
                    }
                },
                error: function(e){
                    var message;
                    if('details' in e.responseJSON) {
                        message = e.responseJSON['details']
                    } else {
                        message = "Hmm, something went wrong and the deletion didn't complete, please try again later"
                    }
                    swal(
                        'Error!',
                        message,
                        'error'
                    ) 
                }
            })
        })
    });



    for(i=0;i<repetitive_elements.length;i++){
        element = repetitive_elements[i]
        addClickListenerForAddMoreElements('.add_more_'+element+'s', element)
        delete_repetitive_element(element);
    }


    function addClickListenerForAddMoreElements(selector, element) {
        $(selector).on('click', function(){
            var title_val = element.charAt(0).toUpperCase() + element.substring(1)
            add_more_repetitive_element(
                title_val,
                element)
        });
    }

    // In the `form` form hide the `share` element if external is deselected
    $('input[name="external"]').on("change", function(){
        if ($(this)[0].checked) {
            $('select[name="share"]').parent().hide()
        } else {
            $('select[name="share"]').parent().show()
        }
    })

    
    // [profile form] position select choices is based on lc choice, so retrieve from backend the choices
    $('#id_lc').on('change', function(){
        $select = $('#id_position')
        $select.html('<option value="" selected="">---------</option>')
        if($(this).val())
        {
            $.ajax({
                url: '/positions/' + $(this).val(),
                success: function(response) {
                    positions = response['details']
                    $.each(positions, function(index, position) 
                    {
                        $select.append('<option value=' + position['pk'] + '>' + position['title'] + '</option>');
                    });
                    $select.removeAttr('disabled')
                }
            })
        } else {
            $select.attr('disabled', 'True')
        }
        
    })


    // Copy to clipboard
    $('.copy-to-clipboard').on('click', function(){
        data_target = $(this).attr('data-target')
        var $temp = $("<input>");
          $("body").append($temp);
          if($(data_target).text()){
            text = $(data_target).text()
          } else {
            text = $(data_target).val()
          }
          $temp.val(text).select();
          document.execCommand("copy");
          $temp.remove();

          alert = $(this).attr("alert")
          console.log(alert)
          $(alert).html("Copied to clipboard")
          $(alert).removeClass('invisible')
    })
    
    initialize_datepicker()
    toggleQuestionChoices()
    
});

var repetitive_elements = ['question', 'paragraph']

var num_paragraphs = 1;
var delete_paragraph_html = '<button type="button" class="close delete_element delete_paragraph" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'

var num_questions = 1;
var delete_question_html = '<button type="button" class="close delete_element delete_question" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'

function initialize_datepicker(){
    // initialize any datepickers
   $('.datepicker').datepicker({
        clearBtn: true
    });
}

function toggleQuestionChoices() {
    // In the `question` form, hide the `choices`, `mutliple` elements
    $('.question select').on('change', function(){
        // $(this).children().removeAttr('selected')
        $(this).children('option[value="' + $(this).val() + '"]').attr("selected", true)
        console.log($(this).children('option[val="' + $(this).val() + '"]'))
        multiple = $(this).parents('.question').children().find('input[type="checkbox"]');
        choices = $(this).parents('.question').children().find('textarea');
        if($(this).val() == 2) {
            multiple.parent().hide()
            choices.parent().hide()
        } else {
            multiple.parent().show()
            choices.parent().show()
        }
    })
}

function add_more_repetitive_element(
    title_val,
    elements_prefix) {

    var delete_identifier = '.delete_' + elements_prefix;
    var main_identifier = '.main_' + elements_prefix;
    // creating an object to pass by reference
    var num_elements_var_name = 'num_' + elements_prefix + 's'
    var title_identifier = '.' + elements_prefix + '_title';
    var delete_element_wrapper_identifier = '.delete_' + elements_prefix + '_wrapper';
    var elements_wrapper = '.' + elements_prefix + 's_wrapper';
    var delete_element_html = window['delete_' + elements_prefix + '_html']

    // only the last element can be deleted, so any
    // delete_element anchor is removed, then a new element is
    // add with a delete_paragraph anchor
    $(delete_identifier).remove()

    var clone = $(main_identifier).clone()
    var main_identifier_class = main_identifier.substring(1)
    clone.removeClass(main_identifier_class)
    clone.find('input').each(function(e){
        if($(this).attr('name')) {
            name = $(this).attr('name').replace(/(.*)\d+(.*)/, "\$1" + window[num_elements_var_name] + "\$2")
            $(this).attr('name', name)
        }
        $(this).val('')
        $(this).removeAttr('checked')
    })
    clone.find('textarea').each(function(e){
        if($(this).attr('name')) {
            name = $(this).attr('name').replace(/(.*)\d+(.*)/, "\$1" + window[num_elements_var_name] + "\$2")
            $(this).attr('name', name)
        }
        $(this).val('')
    })
    clone.find('select').each(function(e){
        if($(this).attr('name')) {
            name = $(this).attr('name').replace(/(.*)\d+(.*)/, "\$1" + window[num_elements_var_name] + "\$2")
            $(this).attr('name', name)
        }
        // $(this).val('')
    })


    window[num_elements_var_name] = window[num_elements_var_name] + 1
    clone.find(title_identifier).html(title_val + ' ' + window[num_elements_var_name])

    clone.find(delete_element_wrapper_identifier).html(delete_element_html)
    clone.addClass(elements_prefix + '_' + window[num_elements_var_name])
    $(elements_wrapper).append(clone)
    $('#id_' + elements_prefix + '-TOTAL_FORMS').attr('value', window[num_elements_var_name])

    initialize_datepicker()
    toggleQuestionChoices()
    delete_repetitive_element(elements_prefix)
}

function delete_repetitive_element(elements_prefix) {
    $('.delete_' + elements_prefix).on('click', function(){
        var delete_html = window['delete_' + elements_prefix + '_html']
        var num_elements_var_name = 'num_' + elements_prefix + 's'
        // delete the leg and update number of legs
        $('.'+elements_prefix+'_' + window[num_elements_var_name]).remove();
        window[num_elements_var_name] -= 1;

        // add remove element for the new last element
        $('.'+elements_prefix+'_' + window[num_elements_var_name]).find('.delete_'+elements_prefix+'_wrapper').html(delete_html)

        // update the input for total paragraphs
        $('#id_'+elements_prefix+'-TOTAL_FORMS').attr('value', window[num_elements_var_name])

        delete_repetitive_element(elements_prefix)
    })
}