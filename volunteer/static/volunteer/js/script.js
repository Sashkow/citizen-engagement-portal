$( document ).ready(function() {

//    addEvent(data.data[i]['id'], data.data[i]['name'], data.data[i]['description'] )

    function addEvent(data, i){

    $('<div>', {class: 'event-block row text-center my-auto align-items-center e-block', style:'height:22vh' }).appendTo($(".events-container"));

    if(data.data[i]['photo_event']){

            $('<div>', { class: 'col-md-4 text-center my_auto', html: '<img src="'+ data.data[i]['photo_event'] +'" href="/event/' + data.data[i]['id'] +'/" style="height:18vh">'}).appendTo($(".e-block"));

        }
        else{

        $('<div>', { class: 'col-md-4 text-center my_auto', html: '<img src="/static/volunteer/images/event.jpg" href="/event/' + data.data[i]['id'] +'/" style="height:18vh">'}).appendTo($(".e-block"));

        }


    $('<div>', {
                    class: 'col-md-8 info' ,
               }).appendTo($('.e-block'));

    $('<div>', {
                    class:"row",
                    html: "<div class='col-md-12 align-items-center'><div><h2><a href='/event/" + data.data[i]['id'] +"/'>" + data.data[i]['name'] + "</a></h2><p>" + data.data[i]['description'] + "</p></div></div>"
               }).appendTo($('.info'))



    if(data.data[i]['subscriber']){
    $('<div>', {class:'row', html: '<div class="col-md-12 text-center my-auto btn-info"><button type="button" class="btn-refollow  btn  dark-primary-color text-primary-color" id="follow"  id_event = "'+ data.data[i]['id'] +'"url_post = "/follow/">Відписатися</button>'}).appendTo($('.info'))

    }
    else{

    $('<div>', {class:'row', html: '<div class="col-md-12 text-center my-auto btn-info"><button type="button" class="btn-follow  btn  dark-primary-color text-primary-color" id="follow"  id_event = "'+ data.data[i]['id'] +'"url_post = "/follow/">Слідкувати</button>'}).appendTo($('.info'))

    }

    $('.btn-info').append('  ')


    if(data.data[i]['part']){

            $('<button> ', { class: "btn-resubscribe btn dark-primary-color text-primary-color", id_event: data.data[i]['id'], url_post: "/subscribe/", text: "Від'єднатися"}).appendTo($('.btn-info'))

    }
    else{
            $('<button> ', { class: "btn-subscribe btn dark-primary-color text-primary-color", id_event: data.data[i]['id'], url_post: "/subscribe/", text: 'Приєднатися'}).appendTo($('.btn-info'))
    }



    $('.btn-info').removeClass('btn-info')
    $(".e-block").removeClass('e-block')
    $(".info").removeClass('info')

    }


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

    $(document).on('change', '#event-type', function(){
        data = {}
        var url = $(this).attr('url_get')
        id = $('option:selected', this).attr('type_id')
        data.type = id

         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK')
                 $(".events-container").empty();

                 if(!jQuery.isEmptyObject(data)){
                        console.log(data)

                        arr = Object.keys(data.data)
                                for(var i = 0; i<arr.length; i++){
//                                    console.log(i)
                                    addEvent(data, i)
                                 }
                  }
                 else{
                 console.log('empty json')

                 $('<h1>', {
                    text: 'За заданими параметрами подій не знайдено',
                 }).appendTo($(".events-container"))
                 }
                 },
             error: function(){
             console.log('error')
            }
         })
    })




    });



