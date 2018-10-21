

$( document ).ready(function() {


    function CheckEmptyField(selector){
        if(selector.val() == ''){
            return false
        }
        else {
            return true
        }
    };

    function FirstRegForm(){
       if(!CheckEmptyField($('input[name="name"]'))){
        console.log('EMPTY NAME')
       }
    }

    $('.category-hint').hover(function(){
        $('.category-tips').toggleClass('d-none');
    })

    $('.category-tips').hover(function(){
        $(this).toggleClass('d-none');
    })


    function readURL(input) {

      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#upload-image').attr('src', e.target.result);
          $('#upload-image').removeClass('d-none');

        }

        reader.readAsDataURL(input.files[0]);
      }
    }


    $(document).on('click', '.filter-setting', function(){

        $('#event_filter').modal('show')

    })

    $(document).on('click', '.open-profile-menu', function(){

        if($(this).attr('active') == "1" ){
            $('.content-container').toggleClass('d-none')
            $('#sidebar').css('display', 'block')
            $(this).attr('active', "0")
        }
        else{
            $('.content-container').toggleClass('d-none')
            $('#sidebar').css('display', 'none')
            $(this).attr('active', "1")
        }

    })

    $(document).on('click', '.usual-reg', function(){
        $('#registration').modal('hide');
        $('#registration-usual').modal('show');
    })

    $(document).on('click', '.usual-log', function(){
        $('#login').modal('hide');
        $('#login-usual').modal('show');
    })

    $(document).on('change', '#event-status', function(){
        data = {}
        var url = $(this).attr('url_get');
        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]

         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');


                 if(!jQuery.isEmptyObject(data)){

                    if(data.html != ""){
                        $(".events-block").empty();
                        $(".events-block").html(data.html);
                    }else{
                        $(".events-block").empty();
                        $('<h1>', { text: 'За заданими параметрами подій не знайдено', }).appendTo($(".events-block"))
                    }


                  }
                 else{
                        $(".events-block").empty();
                        console.log('empty json')

                     $('<h1>', {
                        text: 'За заданими параметрами подій не знайдено',
                     }).appendTo($(".events-block"))
                 }
             },
             error: function(){
             console.log('error')
            }
         })
    })


    $(document).on('click', '.question', function(){
        console.log('here');
         var answer = $(this).attr('answer');
         $('.answer').each(function(index){
            $(this).addClass('d-none');
         })
         $('.' + answer).toggleClass('d-none');
    })


    function InfoEventFilter(){
        var category_id = $('option:selected', '#event-type').attr('type_id');
        var status_id = $('option:selected', '#event-status').attr('status_id');
        if($('.selected_event_task').length){
            if($('.selected_event_task').hasClass('it_is_event')){
                var task_or_event = 'event'
            }else{
                var task_or_event = 'task'
            }
        }else{
            var task_or_event = 'none'
        }
        var state = $('#event-type').attr('state');
        return [category_id, task_or_event, state, status_id]
    }


     function processForm() {
      var data = $('#the_form').serializeArray();
      var url = $('#the_form').attr('post_url');
      var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
      console.log('url')

      data.push(
        {name: 'csrfmiddlewaretoken',  value: csrf_token}
      );
        console.log(data)
      $.ajax({
        type: 'POST',
        url:  url,
        data:  data,
        dataType: 'json'
      }).done(alert("STOP!"))
    }


    $(document).on('click', '#open-reg-modal', function(){

        $('#task-or-event').modal('show')

        $('.task-select').click(function(){
            $('#task-or-event').modal('hide')
            $('#task_register_main').find('#id_events_or_task').removeAttr('checked').addClass('d-none')
            $('#task_register_main').find('#id_status').val('1').addClass('d-none')
            $('#task_register_main').modal('show')
        })

        $('.event-select').click(function(){
            $('#event_register_main').find('#id_events_or_task').addClass('d-none')
            $('#event_register_main').modal('show')
        })
    })



     console.log( "ready!" );

     $(document).on('click', '#mob-filter', function(){
        var data = {}
        var type_id = $('option:selected', '#mob-event-type').attr('type_id');
        var status_id = $('option:selected', '#mob-event-status').attr('status_id');
        if($('.selected_event_task').length){
            if($('.selected_event_task').hasClass('it_is_event')){
                var task_or_event = 'event'
            }else{
                var task_or_event = 'task'
            }
        }else{
            var task_or_event = 'none'
        }
        var state = $('#event-type').attr('state');

        data.type = type_id;
        data.page = 1;
        data.state = state;
        data.task_or_event = task_or_event
        data.status_id = status_id
        var url = $('.filter_event_task').attr('url_get')

        $.ajax({
                 url: url,
                 type :'GET',
                 data:data,
                 cache:true,
                 dataType:'json',
                 success: function(data){
                     console.log('OK');
                     $('#event_filter').modal('hide')

                     if(!jQuery.isEmptyObject(data)){

                        if(data.html != ""){
                            $(".events-block").empty();
                            console.log('not here')
                            $(".events-block").html(data.html);
                        }else{
                            $(".events-block").empty();
                            console.log('here')
                            $('<h1>', { text: 'За заданими параметрами подій не знайдено', }).appendTo($(".events-block"))
                        }

                      }
                     else{
                            $(".events-block").empty();
                            console.log('empty json')

                         $('<h1>', {
                            text: 'За заданими параметрами подій не знайдено',
                         }).appendTo($(".events-block"))
                     }
                 },
                 error: function(){
                 console.log('error')
                }
             })


     })


     $(document).on('click', ".btn-follow", function() {
            var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
            var data = {};
            var event_id = $(this).attr('id_event');
            data.id_event = event_id;
            data['csrfmiddlewaretoken'] = csrf_token;
            data.add = 1;
            var url = $(this).attr('url_post');

            console.log(data)
             $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')
                $('.btn-follow[id_event ="' + event_id + '"]').html('відписатись');
                $('.btn-follow[id_event ="' + event_id + '"]').toggleClass('btn-refollow');
                $('.btn-follow[id_event ="' + event_id + '"]').toggleClass('btn-follow');
             },
             error: function(){
             console.log('error')
             }
             })

    });


    $(document).on('click', ".btn-app-task", function() {
        $('#task_applicate').modal('show')
        console.log($(this).attr('id_event'))
        $('#task_applicate').find('#id_event').val($(this).attr('id_event')).addClass('d-none')
    });


    $(document).on('click', '.btn-refollow', function() {
            var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
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
                 $('.btn-refollow[id_event ="' + event_id + '"]').html('підписатися');
                 $('.btn-refollow[id_event ="' + event_id + '"]').toggleClass('btn-follow');
                 $('.btn-refollow[id_event ="' + event_id + '"]').toggleClass('btn-refollow');
             },
             error: function(){
             console.log('error')
             }
             })

        });



    $(document).on('click', ".btn-subscribe", function() {
            var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
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
                 $('.btn-subscribe[id_event ="' + event_id + '"]').html("відлучитися");
                 $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-resubscribe');
                 $('.btn-subscribe[id_event ="' + event_id + '"]').prev().prop('disabled', true);
                 $('.btn-subscribe[id_event ="' + event_id + '"]').prev().addClass('btn-follow');
                 $('.btn-subscribe[id_event ="' + event_id + '"]').prev().removeClass('btn-refollow');
                 $('.btn-subscribe[id_event ="' + event_id + '"]').prev().text('підписатися');
                 $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-subscribe');


             },
             error: function(){
             console.log('error')
             }
             })

    });


    $(document).on('click', ".btn-resubscribe", function() {
            var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
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
                 $('.btn-resubscribe[id_event ="' + event_id + '"]').html("Приєднатись  ");
                 $('.btn-resubscribe[id_event ="' + event_id + '"]').toggleClass('btn-subscribe');
                 $('.btn-resubscribe[id_event ="' + event_id + '"]').prev().prop('disabled', false);
                 $('.btn-resubscribe[id_event ="' + event_id + '"]').toggleClass('btn-resubscribe');
                 },
                 error: function(){
                 console.log('error')
             }
             })

    });

    $(document).on('change', '#event-type', function(){
        data = {}
        var url = $(this).attr('url_get');
        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]

         $.ajax({
             url: url,
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');


                 if(!jQuery.isEmptyObject(data)){
                    if(data.html != ""){
                        $(".events-block").empty();
                        console.log('not here')
                        $(".events-block").html(data.html);
                    }else{
                        $(".events-block").empty();
                        console.log('here')
                        $('<h1>', { text: 'За заданими параметрами подій не знайдено', }).appendTo($(".events-block"))
                    }

                  }
                 else{
                    $(".events-block").empty();
                    console.log('empty json')

                     $('<h1>', {
                        text: 'За заданими параметрами подій не знайдено',
                     }).appendTo($(".events-block"))
                 }
             },
             error: function(){
             console.log('error')
            }
         })
    })


    $(document).on('click', '.page-item', function(){
        data = {}
        var url = $('#event-type').attr('url_get')
        var page =$(this).attr('page');
        if(page == '...'){
            if ($(this).prev().attr('page') == '1'){
                console.log('start')
                page = Number($(this).next().attr('page')) - 1
                console.log(page)
            }
            else{
                page = Number($(this).prev().attr('page')) + 1
                console.log(page)
            }

        }

        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]


        data.page = page;
        console.log(data)
        $.ajax({
            url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success:function(data){
                console.log('OK');
                if(data.html != ""){
                    $(".events-block").empty();
                    $(".events-block").html(data.html);
                }else{
                    $(".events-block").empty();
                    $('<h1>', { text: 'За заданими параметрами подій не знайдено', }).appendTo($(".events-block"))
                }

                 if(!jQuery.isEmptyObject(data)){

                    $(".events-block").html(data.html);

                  }
                 else{
                        console.log('empty json')

                     $('<h1>', {
                        text: 'За заданими параметрами подій не знайдено',
                     }).appendTo($(".events-block"))
                 }
             },
             error:function(){
                console.log('error')
             }

        })


    })

    $(document).on('click', '.my-volonter-events', function(){
        console.log('.my-volonter-events')
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all'
            data.state = 'volunteer'
            data.page = 1
            data.task_or_event = "none"
            data.status_id = "none"
            data.add_filter = 1;

        }else{
            $('#event-type').attr('state', 'volunteer');
            var url = $('#event-type').attr('url_get');
            var info_filter = InfoEventFilter()
            data.type = info_filter[0];
            data.page = 1;
            data.state = info_filter[2];
            data.task_or_event = info_filter[1];
            data.status_id = info_filter[3];
        }

        console.log(data)
        console.log(url)
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 if( 'filter_html' in data ){
                     $(".dynamic-block").empty()
                     $(".dynamic-block").html(data.filter_html);
                     $(".dynamic-block").append(data.html);
                      $('#event-type').attr('state', 'volunteer');
                 } else {
                    if(!jQuery.isEmptyObject(data)){
                        console.log(data)
                            if(data.html != ""){
                                $(".events-block").empty();
                                console.log('not here')
                                $(".events-block").html(data.html);
                            }else{
                                $(".events-block").empty();
                                console.log('here')
                                $('<h1>', { text: 'Ви не приймаєте участь в подіях', }).appendTo($(".events-block"))
                            }


                          }
                         else{
                                console.log('empty json')

                             $('<h1>', {
                                text: 'За заданими параметрами подій не знайдено',
                             }).appendTo($(".events-block"))
                     }
                 }


             },
             error: function(){
             console.log('error')
             }
        })

    });

        $(document).on('click', '.my-org-events', function(){
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all'
            data.state = 'organizer'
            data.page = 1
            data.task_or_event = "none"
            data.status_id = "none"
            data.add_filter = 1;

        }
        else{
            $('#event-type').attr('state', 'organizer');
            var url = $('#event-type').attr('url_get');
            var info_filter = InfoEventFilter()
            data.type = info_filter[0];
            data.page = 1;
            data.state = info_filter[2];
            data.task_or_event = info_filter[1];
            data.status_id = info_filter[3];
        }

        console.log(data)
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 if( 'filter_html' in data ){
                     $(".dynamic-block").empty()
                     $(".dynamic-block").html(data.filter_html);
                     $(".dynamic-block").append(data.html);
                      $('#event-type').attr('state', 'organizer');
                 }
                 else{
                      if(!jQuery.isEmptyObject(data)){
                        if(data.html != ""){
                            $(".events-block").empty();
                            console.log('not here')
                            $(".events-block").html(data.html);
                        }else{
                            $(".events-block").empty();
                            console.log('here')
                            $('<h1>', { text: 'Ви не організували жодної події', }).appendTo($(".events-block"))
                        }


                      }
                     else{
                            console.log('empty json')

                         $('<h1>', {
                            text: 'За заданими параметрами подій не знайдено',
                         }).appendTo($(".dynamic-block"))
                 }
                 }

             },
             error: function(){
             console.log('error')
             }
        })

    });


    $(document).on('click', '.get-achievements', function(){
        var url = $(this).attr('get_url');
        data = {}
         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                    $(".dynamic-block").empty()
                    $(".dynamic-block").html(data.html)
                 },
             error: function(){
                console.log('error')
             }
             })
        })

$(document).on('click', '.item-menu', function(){
    if ($(this).attr('id')!= 'open-reg-modal'){
             $('.current-menu-item').removeClass('current-menu-item')
             $(this).parent().addClass('current-menu-item')
        }
    if($(window).width()< 768){
        console.log('in')
        $('.content-container').toggleClass('d-none')
        $('#sidebar').css('display', 'none')
        $('.open-profile-menu').attr('active', "1")
    }

})



news_success = function (data) {
    $(".dynamic-block").empty()
     $(".dynamic-block").html(data.filter_html);
     $(".dynamic-block").append(data.html);
     $('#event-type').attr('state', 'news');
}


$(document).on('click', '.news', function(){
    data = {}
    var url = $(this).attr('url_get')
    data.type = 'all_digest';
    data.page = 1;
    data.state = 'news';
    data.task_or_event = 'none';
    data.status_id = 'none';
    data.add_filter = 1;

    history.pushState( {
        url : url,
        data : data,
      }, null, "/wayback/news");


    $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: news_success,
             error: function(){
             console.log('error')
             }
        })

})



         $(document).on('click', '.setting-img', function(){
          var url = $(this).attr('get_url')
          var data = {}

               $.ajax({
                 url: url,
                 type :'GET',
                 data:data,
                 cache:true,
                 success: function(data){
                     console.log('OK');
                     $(".dynamic-block").empty()
                     $(".dynamic-block").html(data.html);
                     if($(window).width()< 768){
                        $('.content-container').toggleClass('d-none')
                        $('#sidebar').css('display', 'none')
                        $('.open-profile-menu').attr('active', "1")
                        $('.current-menu-item').removeClass('current-menu-item');
                    }


                 },
                 error: function(){
                 console.log('error')
                 }
                })
        })


        $(document).on('click', '.btn-event-edit', function(){
            var url = $(this).attr('get_url');
            console.log(url);

            history.pushState( {
                url : url,
                data : {},
              }, null, "/wayback" + url);

            $.ajax({

                 url: url,
                 type :'GET',
                 cache:true,
                 success: function(data){
                     console.log('OK');
                     $(".dynamic-block").empty()
                     $(".dynamic-block").html(data.html);
                 },
                 error: function(){
                 console.log('error')
                 console.log(url)
                 }
                })
        })


//        Editing event
        $(document).on('click', '.send_edit', function(){
            var url = $(this).attr('post_url');
            var event_id = $(this).attr('id_event');
            var name = $('.event-edit-name').val()
            var date = $('#date_event').val()
            var time = $('#time_event').val()
            var address = $('input[name="address"]').val()
            console.log(event_id);
            console.log(name);
            console.log(date);
            console.log(url);
        })



        $(document).on('click', '.event-name',  function(){
            var url = $(this).attr('get_url');
            var data = {}
            console.log(url)
            console.log('click-event-name')
            console.log($(this))
            console.log(url)
            console.log(data)


            history.pushState( {
                url : url,
                data : {},
              }, null, "/wayback"+url);




            $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 console.log('OK2');
                 $(".dynamic-block").empty()
                 $(".dynamic-block").html(data.html);
             },
             error: function(){
             console.log('error')
             }
        })

        })



        notifications_success = function(data) {
            $(".dynamic-block").empty()
            $(".dynamic-block").html(data.html)
        }



        $(document).on('click', '.notifications', function(){



            data = {}
            console.log('notnotnot')
            console.log($(this).attr('get_url'))
            var url = $(this).attr('get_url')

            history.pushState( {
                url : url,
                data : {},
              }, null, "/wayback/notifications");


            $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: notifications_success,
             error: function(){
                console.log('error')
             }
             })

        })



        $(document).on('click', '.filter_event_task', function(){
            console.log('what is it')
            if(!$('.selected_event_task').length){
                $(this).toggleClass('selected_event_task');
            }
            else{
                if($(this).hasClass('selected_event_task')){
                    $(this).toggleClass('selected_event_task');
                }else{
                    $('.selected_event_task').toggleClass('selected_event_task');
                    $(this).toggleClass('selected_event_task');
                }


            }
        })


        $(document).on('click', '.filter_event_task', function(){
            var data = {}
            var url = $(this).attr('url_get')
            console.log(url)
            var info_filter = InfoEventFilter()
            data.type = info_filter[0];
            data.page = 1;
            data.state = info_filter[2];
            data.task_or_event = info_filter[1]
            data.status_id = info_filter[3]
             $.ajax({
                 url: url,
                 type :'GET',
                 data:data,
                 cache:true,
                 dataType:'json',
                 success: function(data){
                     console.log('OK');


                     if(!jQuery.isEmptyObject(data)){

                        if(data.html != ""){
                            $(".events-block").empty();
                            console.log('not here')
                            $(".events-block").html(data.html);
                        }else{
                            $(".events-block").empty();
                            console.log('here')
                            $('<h1>', { text: 'За заданими параметрами подій не знайдено', }).appendTo($(".events-block"))
                        }

                      }
                     else{
                            $(".events-block").empty();
                            console.log('empty json')

                         $('<h1>', {
                            text: 'За заданими параметрами подій не знайдено',
                         }).appendTo($(".events-block"))
                     }
                 },
                 error: function(){
                 console.log('error')
                }
             })
        })





    $(document).on('submit', '.edit-adding-task', function(){
           $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: $(this).attr('action'),
            success: function(data){
                alert('Зміни збережено!')
            },
            error: function(){
                console.log(error)
            }
           })
    })

//    $(document).on('click', '.cancel-task', function(){
//            var url = $(this).attr('post_url');
//            var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
//            var data = {};
//            data['csrfmiddlewaretoken'] = csrf_token;
//            console.log($('.cancel-task[post_url = "' + url + '"]'))
//
//            $.ajax({
//
//                 url: $('#registration').modal('show'),
//                 type :'POST',
//                 data:data,
//                 cache:true,
//                 success: function(data){
//                     console.log('OK');
//                      $('.cancel-task[post_url = "' + url + '"]').remove();
//                     },
//                 error: function(){
//                    console.log('error');
//
//                 }
//            })
//    })


    $(document).on('click', '.open-register', function(){
        $('#registration').modal('show')
    })

    $(document).on('click', '.open-login', function(){
        $('#login').modal('show')
    })

    $('.show-map').mouseenter(function(){

        $('.map-contailer').css('z-index', 800);

    })

    $('.map-contailer').mouseleave(function(){

        $('.map-contailer').css('z-index', -1);


    })


    });


    $(document).on('click', '.get-executers-form', function(){
        var data = {}
        var url = $(this).attr('get_url');
        var event_id = $(this).attr('event_id');
        data.event_id= event_id;
         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                    $(".dynamic-block").append(data.html);
                    $('#modal_executor').modal('show');
                 },
             error: function(){
                console.log('error')
             }
             })

    })



    $(document).on('click', '.select-executor', function(){

        var user_id = $('input[name = "execute"]:checked').val()
        var event_id = $(this).attr('event_id')
        var url = $(this).attr('post_url');
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        data['csrfmiddlewaretoken'] = csrf_token;
        data.user_id = user_id
        data.event_id = event_id
         $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                    $('#modal_executor').modal('hide');
                    $('.get-executers-form').remove();
                 },
             error: function(){
                console.log('error')
             }
             })



    $(document).on('click', '.get-org-tasks', function(){
        var url = $(this).attr('get_url');
        var event_id  =  $(this).attr('event_id');
        var data = {};
        data.event_id = event_id;
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 $(".dynamic-block").append(data.html);
                 $('#event_tasks').modal('show');
                 },
             error: function(){
                console.log('error')
             }
             })
    })





 })

    window.onpopstate = function (event) {
      var url = "";
      var data = {}
      var success_function = null;
      console.log(event.state)
      if(event.state) {
        url = event.state.url;
        data = event.state.data;
        if (url == '/typefilter/'){
            success_function = news_success;
        } else if (url == '/notifications/'){
            success_function = notifications_success;

        } else if ('event/' in url) {
            success_function = function(data){
                 console.log('OK');
                 $(".dynamic-block").empty()
                 $(".dynamic-block").html(data.html);
            }
        } else if ('form' in url){
            success_function = function(data){
                     console.log('OK');
                     $(".dynamic-block").empty()
                     $(".dynamic-block").html(data.html);
            }

        } else {
            success_function = null;
        }
      } else {
        location.href = '/profile/'
        return
      }


        $.ajax({
         url: url,
         type :'GET',
         data:data,
         cache:true,
         success: success_function,
         error: function(){
            console.log('error')
         }

        })
     }















