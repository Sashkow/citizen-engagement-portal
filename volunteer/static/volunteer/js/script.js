$( document ).ready(function() {

     console.log( "ready!" );


    $('.btn-follow').on('click', function(){

            var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
            console.log(csrf_token)
            var data = {};
            var event_id = $(this).attr('id_event');
            console.log(event_id);

            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            var url = $(this).attr('url_post');



             $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
             console.log('OK')
             },
             error: function(){
             console.log('error')
             }
             })
             $(this).html('Відписатись')


    });



});



