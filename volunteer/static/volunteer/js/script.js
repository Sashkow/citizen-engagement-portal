$( document ).ready(function() {

     console.log( "ready!" );


     $(document).on('click', ".btn-follow", function() {
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
            var data = {};
            var event_id = $(this).attr('id_event');

            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            data.add = 1;
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
             $(this).html('Відписатись');
             $(this).toggleClass('btn-refollow');
             $(this).toggleClass('btn-follow');
    });




    $(document).on('click', '.btn-refollow', function() {
    var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
            var data = {};
            var event_id = $(this).attr('id_event');

            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            data.add = 0;
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
             $(this).html('Слідкувати');
             $(this).toggleClass('btn-refollow');
             $(this).toggleClass('btn-follow');
        });



        $(document).on('click', ".btn-subscribe", function() {
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
            var data = {};
            var event_id = $(this).attr('id_event');

            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            data.add = 1;
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
             $(this).html("Від'єднатись");
             $(this).toggleClass('btn-resubscribe');
             $(this).toggleClass('btn-subscribe');
    });


    $(document).on('click', ".btn-resubscribe", function() {
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
            var data = {};
            var event_id = $(this).attr('id_event');

            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            data.add = 0;
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
             $(this).html("Приєднатись  ");
             $(this).toggleClass('btn-resubscribe');
             $(this).toggleClass('btn-subscribe');
    });




    });





