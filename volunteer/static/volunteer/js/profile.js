$( document ).ready(function() {

    $(document).on('click', '#open-reg-modal', function(){

        $('#event_register').modal()
        var data = {}
         $('.btn-next').click(function(){
             var name = $('input[name="name"]').val()
            var type_event = $('option:selected', '#event_task').attr('type_id')
            var category = $('option:selected', '#category').attr('type_id')
            data.name = name;
            data.type=type_event;
            data.category=category;
            $('#event_register').modal('hide')
            if($('option:selected', '#event_task').attr('type_id') == 'event'){
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
                if($('input[name="points_quant"]').val()){data.points_quant = $('input[name="t_points_quant"]').val()}
                if($('input[name="user_email"]').val()){data.email = $('input[name="t_user_email"]').val()}
                if($('#description').val()){data.description_e = $('#description').val()}
                $('.btn-done').unbind().click(function(){
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
//     $('#datetimepicker1').datetimepicker();


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
        id = $('option:selected', this).attr('type_id');
        data.type = id;
        data.page = 1;
        data.state = $('#event-type').attr('state');
         $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success: function(data){
                 console.log('OK');
                 $(".events-container").empty();

                 if(!jQuery.isEmptyObject(data)){

                    $(".events-container").html(data.html);

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


    $(document).on('click', '.page-item', function(){
        console.log("Page-click");
        data = {}
        var url = $('#event-type').attr('url_get')
        var type_id = $('option:selected', '#event-type').attr('type_id');
        var page =$(this).attr('page');
        var state = $('#event-type').attr('state');
        console.log(data)
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

        console.log(page);
        console.log('Here!')
        console.log(type_id);
        console.log(url);

        data.page = page;
        data.type = type_id;
        data.state = state;

        $.ajax({
            url: url,
             type :'GET',
             data:data,
             cache:true,
             dataType:'json',
             success:function(data){
                console.log('OK');
                $(".events-container").empty();

                 if(!jQuery.isEmptyObject(data)){

                    $(".events-container").html(data.html);

                  }
                 else{
                        console.log('empty json')

                     $('<h1>', {
                        text: 'За заданими параметрами подій не знайдено',
                     }).appendTo($(".events-container"))
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
        data.type = 'all';
        data.page = 1;
        data.state = 'volunteer';
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

                        $(".events-container").html(data.html);
                        $('#event-type').attr('state', 'volunteer');

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

    });

        $(document).on('click', '.my-org-events', function(){
        var csrf_token = $('.profile_info [name = "csrfmiddlewaretoken"]').val();
        var data = {};
        var url = $('#event-type').attr('url_get');
        data.type = 'all';
        data.page = 1;
        data.state = 'organizer';
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

                        $(".events-container").html(data.html);
                        $('#event-type').attr('state', 'organizer');

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

    });



    });



