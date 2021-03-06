document.addEventListener('DOMContentLoaded', (event) => {
    var time = '';
    var date = '';
    var action = '';
    // $('.start').click(function(){
    //     action = 'start';
    //     var target = $(this);
    //     target.attr('id', 'is_active');
    //     date = target.parent().attr('class');
    //     $('.modal__content').append('<input id="active_time" class="active" type="time" min="0" max="23" style="padding: 0; width: 100%; font-size: 72px;">');
    //     $('#active_time').val(target.text());
    //     if(target.text()[0] == '0') {
    //         time = target.text().match('^0([0-9]+:[0-9]+)')
    //     }
    //     $('.modal').fadeIn();
    // });

    // $('.end').click(function(){
    //     if($(this).parent().children('.start').text()){
    //         action = 'end';
    //         var target = $(this);
    //         target.attr('id', 'is_active');
    //         date = target.parent().attr('class');
    //         $('.modal__content').append('<input id="active_time" type="time" min="0" max="23" style="padding: 0; width: 100%; font-size: 72px;">');
    //         $('#active_time').val(target.text());
    //         if(target.text()[0] == '0') {
    //             time = target.text().match('^0([0-9]+:[0-9]+)')
    //         }
    //         $('.modal').fadeIn();
    //     }
    // });

    $('.start').click(function(){
        changeTime($(this));
    });

    $('.end').click(function(){
        if($(this).parent().children('.start').text()){
            changeTime($(this));
        }
    });

    function changeTime(object) {
        action = object.attr('class').substring(0, object.attr('class').length);
        // alert(action);
        var target = object;
        target.attr('id', 'is_active');
        date = target.parent().attr('class');
        $('.modal__content').append('<input id="active_time" class="active" type="time" min="0" max="23" style="padding: 0; width: 100%; font-size: 72px;">');
        $('#active_time').val(target.text());
        if(target.text()[0] == '0') {
            time = target.text().match('^0([0-9]+:[0-9]+)')[1]
        } else {
            time = target.text();
        }
        $('.modal').fadeIn();
    }

    $('.modal__bg').click(function(){
        var new_time = $('#active_time').val();
        var result = false;
        var tmpDate= date.split('-')
        var tmpTime= new_time.split(':')
        var date1 = new Date();
        // 今月以前かで判定
        if(Number(tmpDate[0]) <= date1.getFullYear() && Number(tmpDate[1]) <= date1.getMonth() + 1) {
            // 今日以前か判定
            if(Number(tmpDate[2]) < date1.getDate()) {
                result = true;
                // 現在時以前か判定
            } else if(Number(tmpDate[2]) == date1.getDate()) {
                if(Number(tmpTime[0]) < date1.getHours() || Number(tmpTime[0]) == date1.getHours() && Number(tmpTime[1]) <= date1.getMinutes()) {
                    result = true;
                }
            }
        }
        
        if(result && time != new_time) {
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
                action = '';
            });
        } else {
            $('#active_time').remove();
            $('#is_active').removeAttr('id');
            $('.modal').removeAttr('id');
            $('.modal').fadeOut();
        }

    });
});