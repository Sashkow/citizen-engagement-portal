$( document ).ready(function() {



    $(document).on('click', 'button.edit-profile-send', function(){

        var digest_data = {}
        $("input[type='checkbox']").each(function(index){
            var type_id = $(this).attr('type_id')
            console.log(type_id)
            digest_data[String(type_id)] = $(this).is(':checked');
        })
        var url = $('button.edit-profile-send').attr('post_url')
        var csrf_token = $('input[name = "csrfmiddlewaretoken"]').val();
        digest_data['csrfmiddlewaretoken'] = csrf_token;
        console.log(digest_data)
        $.ajax({
            data : digest_data,
            type : 'POST',
            url: url,
            success: function(data){
                $('form.edit-profile-send').submit()
            },
            error:function(){
                console.log('error');
            }

            })
    })


    $uploadCrop = $('.upload-image').croppie({
                    enableExif: true,
                    viewport: {
                        width: 156,
                        height: 176,
                    },
                    boundary: {
                        width: 200,
                        height: 300
                    }
                });

                function readFile(input) {
                    if (input.files && input.files[0]) {
                        var reader = new FileReader();

                        reader.onload = function (e) {
                            $('.upload-image').addClass('ready');
                            $uploadCrop.croppie('bind', {
                                url: e.target.result
                            }).then(function(){
                                console.log('jQuery bind complete');
                            });

                        }

                        reader.readAsDataURL(input.files[0]);
                    }
                    else {
                        swal("Sorry - you're browser doesn't support the FileReader API");
                    }
                }



                $('#upload').on('change', function(){

                  readFile(this);

                      $('.upload-result').on('click', function (ev) {
                        $uploadCrop.croppie('result', {
                            type: 'canvas',
                            size: 'original'
                        }).then(function (resp) {
                            console.log(resp);
                            var strImage = resp.replace(/^data:image\/[a-z]+;base64,/, "");
                            console.log(strImage)
                            var blob = b64toBlob(strImage, 'image/png');
                            var blobUrl = URL.createObjectURL(blob);
                            console.log(blobUrl);
                            console.log(typeof(blob));
                            $('#image').val(blob);
                            console.log( $('#image').val());
                            })
                        })

                })

})