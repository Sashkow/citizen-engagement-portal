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

//    $('.category-hint').click(function(){
//        alert('fy');
//        $('.category-tips').removeClass('d-none');
//    })

var tipVisibility = 0;
    $(document).on("click", function(){
        if (tipVisibility!=1){
        $('.fp-slidesNav ul').css('visibility', 'hidden');
        $('.category-tip').css('visibility', 'hidden');
        $('.category-tips').css('visibility', 'hidden');
        }
        tipVisibility++;
    });

     $('.category-hint').on("click" ,function(){
            $('.fp-slidesNav ul').css('visibility', 'visible');
            $('.category-tip').css('visibility', 'visible');
            $('.category-tips').css('visibility', 'visible');
            tipVisibility=1;
        });

    $('.category-tips').on("click" ,function(){

            tipVisibility=1;
        });
         var myFullpage = new fullpage('#fullpage', {

                sectionsColor: ['#491c65', '#fff', '#f5ec9bff', '#cad893ff', '#7bd5b4ff','#bee6d2ff'],

	            menu: '#myMenu',
                slidesNavigation: true,
                <!--&lt;!&ndash;scrollBar: true&ndash;&gt;-->

            });
            data = {}
    var url = $(this).attr('url_get')
    if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all'
            data.state = 'news'
            data.page = 1
            data.task_or_event = "none"
            data.status_id = "none"
            data.city_id = "none"
            data.add_filter = 1;

        }else{
            $('#event-type').attr('state', 'news');
            var url = $('#event-type').attr('url_get');
            var info_filter = InfoEventFilter()
            data.type = info_filter[0];
            data.page = 1;
            data.state = info_filter[2];
            data.task_or_event = info_filter[1];
            data.status_id = info_filter[3];
            data.city_id = info_filter[4];
            data.add_filter = 1;
        }
            filterEvents(data, url, 'news');





//     $('.task-event-hint').hover(function(){
//        $('.event-or-task-tips').toggleClass('d-none');
//    })

//    $('.event-or-task-tips').hover(function(){
//        $(this).toggleClass('d-none');
//    })


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
        else{_
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

    // event search


    $(document).on('keyup', '#event-search', function () {
        data = {}
        var url = $(this).attr('url_get');
        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]
        data.city_id = filter_info[4]
        data.add_filter = 1;
        data.search = $(this).val()
        console.log(data);

         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');
                 console.log(url);
                 console.log(data);

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

    // end event search

    $(document).on('change', '#event-city', function(){
        data = {}
        var url = $(this).attr('url_get');
        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]
        data.city_id = filter_info[4]
        data.add_filter = 1;
        console.log(data);
         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');
                 console.log(url);
                 console.log(data);


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

    $(document).on('change', '#event-status', function(){
        data = {}
        var url = $(this).attr('url_get');
        filter_info = InfoEventFilter()
        data.type = filter_info[0];
        data.page = 1;
        data.state = filter_info[2];
        data.task_or_event = filter_info[1]
        data.status_id = filter_info[3]
        data.city_id = filter_info[4]
        data.add_filter = 1;

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
        var city_id = $('option:selected', '#event-city').attr('city_id');
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
        return [category_id, task_or_event, state, status_id, city_id]
    }


     function processForm() {
      var data = $('#the_form').serializeArray();
      var url = $('#the_form').attr('post_url');
       var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
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
//            hide enent_or_tast menu
            $('#event_register_main').find('#id_events_or_task').addClass('d-none')
//          show register envent menu
            $('#event_register_main').modal('show')
        })
    })



     console.log( "ready!" );

     $(document).on('click', '#mob-filter', function(){
        var data = {}
        var city_id = $('option:selected', '#mob-event-city').attr('city_id');
        var category_id = $('option:selected', '#mob-event-type').attr('type_id');
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
        var state = $('#mob-event-type').attr('state');




        data.type = category_id;
        data.page = 1;
        data.state = state;
        data.task_or_event = task_or_event;
        data.status_id = status_id;
        data.city_id = city_id;
        data.add_filter = 1;
        var url = $('.filter_event_task').attr('url_get');

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


    $(document).on('click', ".btn-app-task", function() {
        // mark test field id_event as hidden and fill it with value which is id_event attribute on the button itself
        $('#task_applicate').modal('show')
        //        console.log($(this).attr('id_event'))
        $('#task_applicate').find('#id_event').val($(this).attr('id_event')).addClass('d-none')
        document.getElementById("id_event").value = $(this).attr('id_event');
    });



    $(document).on('click', ".btn-subscribe", function() {
            var csrf_token = $('input[name = "csrfmiddlewaretoken"]').last().val();
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
//             $('.btn-subscribe[id_event ="' + event_id + '"]').html("скасувати участь");
//             $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-resubscribe');
//             $('.btn-subscribe[id_event ="' + event_id + '"]').prev().prop('disabled', true);
//             $('.btn-subscribe[id_event ="' + event_id + '"]').prev().addClass('btn-follow');
//             $('.btn-subscribe[id_event ="' + event_id + '"]').prev().removeClass('btn-refollow');
//             $('.btn-subscribe[id_event ="' + event_id + '"]').prev().text('підписатися');
//             $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-app-task');
//             $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-subscribe');
             $('.btn-resubscribe[id_event ="' + event_id + '"]').show();
             $('.btn-subscribe[id_event ="' + event_id + '"]').hide();
             $('.task_price[id_event ="' + event_id + '"]').hide();




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
//                 $('.btn-resubscribe[id_event ="' + event_id + '"]').html("долучитися");
//                 $('.btn-resubscribe[id_event ="' + event_id + '"]').toggleClass('btn-subscribe');
//                 $('.btn-resubscribe[id_event ="' + event_id + '"]').prev().prop('disabled', false);
//                 $('.btn-subscribe[id_event ="' + event_id + '"]').toggleClass('btn-app-task');
//                 $('.btn-resubscribe[id_event ="' + event_id + '"]').toggleClass('btn-resubscribe');
                   $('.btn-resubscribe[id_event ="' + event_id + '"]').hide();
                   $('.btn-subscribe[id_event ="' + event_id + '"]').show();
                   $('.task_price[id_event ="' + event_id + '"]').show();


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
        data.city_id = filter_info[4]
        data.add_filter = 1;
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
        data.city_id = filter_info[4]
        data.add_filter = 1;
        data.search = $(this).val()


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
        var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
        var data = {};
        if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all'
            data.state = 'volunteer'
            data.page = 1
            data.task_or_event = "none"
            data.status_id = "none"
            data.city_id = "none"
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
            data.city_id = info_filter[4];
            data.add_filter = 1;
        }

        console.log(data)
        console.log(url)
        filterEvents(data,url,'volunteer');

    });

        $(document).on('click', '.my-org-events', function(){
        var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
        var data = {};

        if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all';
            data.state = 'organizer';
            data.page = 1;
            data.task_or_event = "none";
            data.status_id = "none";
            data.city_id = "none";
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
            data.city_id = info_filter[4];
            data.add_filter = 1;

        }

        console.log(data)
        filterEvents(data,url,'organizer');

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
                     document.getElementsByClassName("event-navigation")[0].style.display = "none";

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
     //$(".dynamic-block").html(data.filter_html);
     $(".dynamic-block").append(data.html);
     $('#event-type').attr('state', 'news');
     $('.current-menu-item').removeClass('current-menu-item')
     $('.news').parent().addClass('current-menu-item')
}


$(document).on('click', '.news', function(){
    data = {}
    var url = $(this).attr('url_get')
    if( !$('#event-type').length ){
            var url = "/typefilter/"
            data.type = 'all'
            data.state = 'news'
            data.page = 1
            data.task_or_event = "none"
            data.status_id = "none"
            data.city_id = "none"
            data.add_filter = 1;

        }else{
            $('#event-type').attr('state', 'news');
            var url = $('#event-type').attr('url_get');
            var info_filter = InfoEventFilter()
            data.type = info_filter[0];
            data.page = 1;
            data.state = info_filter[2];
            data.task_or_event = info_filter[1];
            data.status_id = info_filter[3];
            data.city_id = info_filter[4];
            data.add_filter = 1;
        }


    history.pushState( {
        url : url,
        data : data,
      }, null, "/wayback/news");

    filterEvents(data, url, 'news')
//    $.ajax({
//             url: url,
//             type :'GET',
//             data:data,
//             cache:true,
//             success: news_success,
//             error: function(){
//             console.log('error')
//             }
//        })

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
                     document.getElementsByClassName("event-navigation")[0].style.display = "none";
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
            document.getElementsByClassName("event-navigation")[0].style.display = "none";

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
                 document.getElementsByClassName("event-navigation")[0].style.display = "none";
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
            document.getElementsByClassName("event-navigation")[0].style.display = "none";
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


        $(document).on('click', '.themap', function(){
            data = {}
            console.log('mapmap')
            console.log($(this).attr('get_url'))
            var url = $(this).attr('get_url')

            history.pushState( {
                url : url,
                data : {},
              }, null, "/wayback/map");


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
            data.city_id = info_filter[4]
            data.add_filter = 1;
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
        var csrf_token = $(' input[name = "csrfmiddlewaretoken"]').last().val();
        var data = {};
        data['csrfmiddlewaretoken'] = csrf_token;
        data.user_id = user_id
        data.event_id = event_id
        console.log(event_id);
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
        console.log(event_id)
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
        if (location.href.includes('/map/')) {
            location.href = '/map/'
            retrun
        } else{
            location.href = '/profile/'
            return
        }

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



function filterEvents(data, url, state){
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 console.log(data);
                 if( 'filter_html' in data & data.html != "" ){
                     $(".dynamic-block").empty()
                     //$(".dynamic-block").html(data.filter_html);
                     $(".dynamic-block").append(data.html);
                      $('#event-type').attr('state', state);
                 }
                 else{
                      if(!jQuery.isEmptyObject(data)){
                        if(data.html != ""){
                            $(".events-block").empty();
                            console.log('not here')
                            $(".events-block").html(data.html);
                        }else{
                            $(".dynamic-block").empty()
                            console.log('here')
                            $('<h1>', { text: 'За заданими параметрами подій не знайдено :(', }).appendTo($(".dynamic-block"))
                        }


                      }
                     else{
                            console.log('empty json')

                         $('<h1>', {
                            text: 'За заданими параметрами подій не знайдено :(',
                         }).appendTo($(".dynamic-block"))
                 }
                 }
                 document.getElementsByClassName("event-navigation")[0].style.display = "flex";

             },
             error: function(){
             console.log('error')
             }
        })
        }
