$(document).ready(function(){
    var aURL = window.location.origin;
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function generate_request(form_data)
    {
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        
        $.ajax({
            type: "POST",
            url: aURL + '/generate',
            data: form_data,
            dataType: "JSON",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (response) {
                url = response.url;
                if (url != '') {
                    swal({
                        title: 'Success',
                        text: 'Ready to Download',
                        type: 'success'
                    }).then(function(){
                        $('#inp_name').val('');
                        $('#inp_author').val('');
                        $('#inp_description').val('');
                        $('#inp_version').val('1.0');
                        window.open(window.location.origin + url)
                    });
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    }

    $('#btn_generate').on('click', function() {
        var module_name = $('#inp_name').val();
        var author = $('#inp_author').val();
        var description = $('#inp_description').val()
        var version = $('#inp_version').val();

        if (module_name == '' || author == '' || description == '' || version == '') {
            swal(
                'Oops..',
                'Please filling out empty fields',
                'warning'
            );
            return false;
        }
        
        var form_data = {
            'csrftoken': csrftoken,
            'module_name': module_name,
            'author': author,
            'description': description,
            'version': version
        };

        swal({
            title: 'Start Generate',
            text: "Are you sure?",
            type: 'info',
            showCancelButton: true,
            confirmButtonText: 'Generate It!',
            cancelButtonText: 'No, cancel!',
            confirmButtonClass: 'btn blue darken-3',
            cancelButtonClass: 'btn red lighten-1',
            buttonsStyling: false,
            showLoaderOnConfirm: true,
            allowOutsideClick: false
            }).then(function () {
                generate_request(form_data);
            }, function (dismiss) {
                if (dismiss === 'cancel') {
                    swal.close();
                }
        });
    });

    $("#inp_name").on('keydown', function(e) {
        var code = e.keyCode;
        if (code == 32) {
            return false;
        }
    });
});