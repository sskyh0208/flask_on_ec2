document.addEventListener('DOMContentLoaded', (event) => {
    var time = '';
    var date = '';
    var action = '';
    $('.start').click(function(){
        action = 'start';
        var target = $(this);
        var time = target.text();
        target.attr('id', 'is_active');
        date = target.parent().attr('class');
        $('.modal__content').append('<input id="active_time" class="active" type="time" min="0" max="23" style="padding: 0; width: 100%; font-size: 72px;">');
        $('#active_time').val(time);
        $('.modal').fadeIn();
    });

    $('.end').click(function(){
        if($(this).parent().children('.start').text()){
            action = 'end';
            var target = $(this);
            time = target.text();
            target.attr('id', 'is_active');
            date = target.parent().attr('class');
            $('.modal__content').append('<input id="active_time" type="time" min="0" max="23" style="padding: 0; width: 100%; font-size: 72px;">');
            $('#active_time').val(time);
            $('.modal').fadeIn();
        }
    });

    $('.modal__bg').click(function(){
        var new_time = $('#active_time').val();
        if(time != new_time) {
            $.getJSON('/time_edit', {
                date: date,
                time: new_time,
                action: action
            }, function(data){
                if(!$('#is_active').find('span').length){
                    $('#is_active').append('<span></span>');
                }
                // 修正した時間を入れる
                $('#is_active').children('span').text(data['time']);

                // 出勤と退勤に時刻があって、合計に時刻がない場合に要素追加
                if($('#is_active').parent().children('.end').text() && $('#is_active').parent().children('.start').text() && !$('#is_active').parent().children('.total').text()) {
                    $('#is_active').parent().children('.total').append('<span></span>');
                }
                $('#is_active').parent().children('.total').children('span').text(data['total']);
                $('#active_time').remove();
                $('#is_active').removeAttr('id');
                $('.modal').removeAttr('id');
                $('.modal').fadeOut();
            });
        } else {
            $('#active_time').remove();
            $('#is_active').removeAttr('id');
            $('.modal').removeAttr('id');
            $('.modal').fadeOut();
        }

    });
});