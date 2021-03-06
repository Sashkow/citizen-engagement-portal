$( document ).ready(function() {

function animateValue(obj, start, end, duration) {
    var range = end - start;
    var current = start;
    var increment = end > start? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var timer = setInterval(function() {
        current += increment;
        obj.html(current)
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}


    $(document).on('click', '.change-league', function(){
        var data = {}
        data.id = $(this).attr('legaues_id')
        var url = $(this).attr('get_url')
//        $(this).prop('disabled', true);
        console.log($(this))

        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')
                $('.dynamic-block').empty()
                $(".dynamic-block").html(data.html);
//                $('.change-league:disabled').prop('disabled', false);
             },
             error: function(){
                console.log('error')
             }
         })
    });

    $(document).on('click', '.buy-achieve', function(){
        data = {}
        var csrf_token = $('input[name = "csrfmiddlewaretoken"]').val();
        var url = $(this).attr('post_url');
        var id_achieve = $(this).attr('achieve_id');
        data['csrfmiddlewaretoken'] = csrf_token;
        data.id = id_achieve;


        $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')

                if( 'error' in data){
                    $('#error-buying').modal()
                    $('p.error-currency').text(data.error)
                    $('img.error-currency').attr('src', data.url_currency)
                    }else if('success' in data){

                        var needed_object = $('.ach-container[achieve_id = '+ id_achieve +' ]')
                        needed_object.empty();
                        needed_object.append(data.html);
                        if('ach_in_current' in data){
                                var ach_in_league = parseInt(($('.own-progress-bar').children().first().next().html()))
                                var per_one = 100/ach_in_league
                                var progress_width = $(".own-progress-league").width() / $('.own-progress-league').parent().width() * 100;
                                var new_progress_width = progress_width + per_one
                                if (new_progress_width>5*per_one){
                                    new_progress_width = 5*per_one;
                                }
                                $('.progress_state').hide()
                                $('.own-progress-league').animate({ width: new_progress_width + '%' }, 'slow', function(){
                                    $('.progress_state').show()
                                })

                                $('.quant-ach').html(parseInt($('.quant-ach').html()) + 1)
                        }

                            $.each(data.curr_quant, function( k, v ) {
                                console.log(typeof(k))
                                var curr_obj = $('.curr_quat[id_curr = "'+ k+ '"')
                                var start = parseInt(curr_obj.html())
                                var end = start - parseInt(v)
                                console.log(curr_obj);
                                console.log(start);
                                console.log(end);
                                animateValue(curr_obj, start, end, 1000)
                            });




                        if('new_league' in data){
                            console.log(data)
                            console.log(data.all_info.background_color)

                            var b_image = "url(" + data.all_info.background_image + ")"
                            var curr_bord = data.all_info.color_current_border

                            $('#sidebar').css({"background-color": data.all_info.background_color })
                            $('.side-background').css({"opacity": data.design_info.background_opacity , "background-image" : b_image })

                            var b_image = data.all_info.background_image

                            $("head").append('<style type="text/css"></style>');
                            var newStyleElement = $("head").children(':last');
                            newStyleElement.html('.current-menu-item{border-left: 1.3vh solid '+ data.design_info.color_current_border +';}');
                            newStyleElement.append('.current-menu-item{background-image: linear-gradient( 120deg, '+ data.design_info.color_current_grad1 +', ' + data.design_info.color_current_grad2 + ', ' +data.design_info.color_current_grad1 +');}');
                            newStyleElement.append('p.ribbon{ color: '+ data.design_info.color_league_txt +';}');
                            newStyleElement.append('.volunteer-name{ color: '+ data.design_info.color_volunteer_name +';}');
                            newStyleElement.append('.curr_quat{ color: '+ data.design_info.color_menu_item +';}');
                            newStyleElement.append('div.current-menu-item p.item-menu{ '+ data.design_info.color_current_text +'!important;}');
                            newStyleElement.append(' .photo-user{ width:'+ data.all_info.img_user_width +';}');
                            newStyleElement.append(' .photo-user{ right:'+ data.all_info.img_user_height +';}');
                            newStyleElement.append(' .photo-user{ height:'+ data.all_info.img_user_height_corr +';}');
                            newStyleElement.append('.notif-col{ color:'+ data.design_info.color_not_text +';}');
                            newStyleElement.append('.item-menu{ color:'+ data.design_info.color_menu_item +';}');

                            $('p.ribbon').text(data.new_league)
                            $('#front-image').attr('src', data.design_info.photo_frame)
                            $('#back-image').attr('src', data.all_info.league_image)

                            $('#new-league').modal()
                            $('.new-league').text(data.new_league)
                            $('.progress_state').hide()
                            $('.own-progress-league').animate({ width: 0 }, 'slow', function(){
                                    $('.progress_state').show()
                            })

                            $('.quant-ach').html(0)

                        }
                 }

             },
             error: function(){
                console.log('error')
             }
         })

    })

})