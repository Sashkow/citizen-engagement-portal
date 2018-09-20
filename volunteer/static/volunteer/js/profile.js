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

        $('#event_register').modal('show')
        var data = {}
         $('.btn-next').click(function(){
            var name = $('input[name="name"]').val()
            var type_event = $('option:selected', '#event_task').attr('type_id')
            var category = $('option:selected', '#category').attr('type_id')
            data.name = name;
            data.type=type_event;
            data.category=category;
            $('#event_register').modal('hide')
            if($('option:selected', '#even t_task').attr('type_id') == 'event'){
                $('#event_e_register').modal()
                $(document).on('change', '#event_status', function(){
                    if ($('option:selected', '#event_status').attr('status_id') == "1"){
                            $('.add-org-task').removeClass('d-none')
                            $('.more-tasks').removeClass('d-none')
                            $('.more-tasks').unbind().click(function(){
                                console.log('click')
                                 $('.task-info:first').clone().appendTo(".add-org-task")

                            })
                            }
                        else{
                            console.log('in')
                             var add_element = $('.task-info:first').clone()
                            $('.add-org-task').empty()
                            $(add_element).appendTo('.add-org-task')
                            $('.add-org-task').addClass('d-none')
                            $('.more-tasks').addClass('d-none')
                        }
                    })
                $('#btn-done').unbind().click(function(){
                        if($('option:selected', '#event_status').attr('status_id')){data['status'] = $('option:selected', '#event_status').attr('status_id')}
                        if($('input[name="address"]').val()){data['address']= $('input[name="address"]').val()}
                        if($('input[name="date"]').val()){data.date = $('input[name="date"]').val()}
                        if($('input[name="from"]').val()){data.from = $('input[name="from"]').val()}
                        if($('input[name="to"]').val()){data.to = $('input[name="tp"]').val()}
                        if($('input[name="points_quant"]').val()){data.points_quant = $('input[name="points_quant"]').val()}
                        if($('input[name="user_email"]').val()){data.email = $('input[name="user_email"]').val()}
                        if($('#description_e').val()){data.description_e = $('#description_e').val()}
                        if($('option:selected', '#event_status').attr('status_id') == '1'){
                            arr = []
                            numb = 0
                            $('.task-info').each(function(index){
                                dict = {}
                                name_task = $(this).find( 'input.name_task' ).val()
                                point_task = $(this).find( 'input.point_task' ).val()
                                descr_task = $(this).find( '.descr_task' ).val()
                                dict.name_task = name_task
                                dict.point_task = point_task
                                dict.descr_task = descr_task
                                arr.push(dict)
                                numb = numb+1
                            })
                            data['task_arr'] = arr
                            data['numb'] = numb
                        }
                        var url = $('#event_e_register').attr('post_url')
                        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
                        data['csrfmiddlewaretoken'] = csrf_token;
                        console.log(data)
                        $.ajax({
                             url: url,
                             type :'POST',
                             data:data,
                             cache:true,
                             success: function(data){
                             console.log('OK')
                             $('#event_e_register').modal('hide')

                             },
                             error: function(){
                             console.log('error')
                             }
                         })
                })
            }else{
                $('#task_register').modal()
                console.log('alalal')
                $('.btn-done').unbind().click(function(){
                if($('input[name="t_points_quant"]').val()){data.points_quant = $('input[name="t_points_quant"]').val()}
                    console.log($('input[name="t_points_quant"]').val())
                    if($('input[name="user_email"]').val()){data.email = $('input[name="t_user_email"]').val()}
                    if($('#description').val()){data.description_e = $('#description').val()}
                    var url = $('#event_e_register').attr('post_url')
                        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
                        data['csrfmiddlewaretoken'] = csrf_token;
                        console.log(data)
                        $.ajax({
                             url: url,
                             type :'POST',
                             data:data,
                             cache:true,
                             success: function(data){
                             console.log('OK')
                             $('#task_register').modal('hide')

                             },
                             error: function(){
                             console.log('error')
                             }
                         })
                })
            }
        })
     })


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
             $(this).prev().prop('disabled', true);
             $(this).prev().addClass('btn-follow');
             $(this).prev().removeClass('btn-refollow');
             $(this).prev().text('Слідкувати');
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
             $('.btn-follow').prop('disabled', false);
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
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');


                 if(!jQuery.isEmptyObject(data)){
                    $(".events-block").empty();

                    $(".events-block").html(data.html);

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
            console.log('It is bed')
            if ($(this).prev().attr('page') == '1'){
                console.log('start')
                page = Number($(this).next().attr('page')) - 1
                console.log(page)
            }
            else{
                console.log('end')
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

        $.ajax({
            url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success:function(data){
                console.log('OK');
                $(".events-block").empty();

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
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        var url = $('#event-type').attr('url_get');
        var info_filter = InfoEventFilter()
        data.type = info_filter[0];
        data.page = 1;
        data.state = info_filter[2];
        data.task_or_event = info_filter[1];
        data.status_id = info_filter[3];
        console.log(data)
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 if(!jQuery.isEmptyObject(data)){
                        console.log(data)

                        $(".events-block").html(data.html);
                        $('#event-type').attr('state', 'volunteer');

                      }
                     else{
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

    });

        $(document).on('click', '.my-org-events', function(){
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        var url = $('#event-type').attr('url_get');
        var info_filter = InfoEventFilter()
        data.type = info_filter[0];
        data.page = 1;
        data.state = info_filter[2];
        data.task_or_event = info_filter[1];
        data.status_id = info_filter[3];
        console.log(data)
        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 if(!jQuery.isEmptyObject(data)){
                        $(".events-block").html(data.html);
                        $('#event-type').attr('state', 'organizer');

                      }
                     else{
                            console.log('empty json')

                         $('<h1>', {
                            text: 'За заданими параметрами подій не знайдено',
                         }).appendTo($(".dynamic-block"))
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
             $(this).parent().parent().addClass('current-menu-item')
        }

})

$(document).on('click', '.news', function(){
    data = {}
    var url = $(this).attr('url_get')
    data.type = 'all_digest';
    data.page = 1;
    data.state = 'news';
    data.task_or_event = 'none';
    data.status_id = 'none';
    data.add_filter = 1;


    $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 $(".dynamic-block").empty()
                 $(".dynamic-block").html(data.filter_html);
                 $(".dynamic-block").append(data.html);
                 $('#event-type').attr('state', 'organizer');
             },
             error: function(){
             console.log('error')
             }
        })

})



        $(document).on('click', '.my-events', function(){
           $(this).parent().parent().next().removeClass('d-none');
           $(this).parent().parent().next().next().removeClass('d-none');
           $('.my-org-events, .my-volonter-events').click(function(){
                $('.my-events').parent().parent().addClass('current-menu-item');
                $('.my-events').parent().parent().next().addClass('d-none');
                $('.my-events').parent().parent().next().next().addClass('d-none');
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
                 },
                 error: function(){
                 console.log('error')
                 }
                })
        })


        $(document).on('click', '.btn-event-edit', function(){
            var url = $(this).attr('get_url');
            console.log(url);
                $.ajax({

                     url: url,
                     type :'GET',
                     cache:true,
                     success: functigon(data){
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
            $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                 console.log('OK');
                 $(".dynamic-block").empty()
                 console.log(data)
                 $(".dynamic-block").html(data.html);
//                 $('#event-type').attr('state', 'organizer');
             },
             error: function(){
             console.log('error')
             }
        })

        })



        $(document).on('click', '.notifications', function(){
            data = {}
            console.log('notnotnot')
            var url = $(this).attr('get_url')
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
                        $(".events-block").empty();

                        $(".events-block").html(data.html);

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
        console.log(filter_info)
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
                    $(".events-block").empty();

                    $(".events-block").html(data.html);

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

    $(document).on('submit', '#the_form', function(){
        console.log('send edited info');
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        $(this).append(csrf_token);
        return True;

    })


    });



