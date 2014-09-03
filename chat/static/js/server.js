$(function() {
    var toggle = 1;
    $('.button-background').click(function() {
        if (toggle) {
            var time = 50;
            function display() {
                $('.button-item:hidden').first().slideDown(time, display);
                time += 20;
            }
            display();
        } else {
            var time = 50
            function hide() {
                $('.button-item:visible').last().slideUp(time, hide);
                time += 20;
            }
            hide();
            $('.message-box').empty();
            $('.server-dashboard').slideUp(500);
        }
        toggle = 1 - toggle;
    });

    $('.button-item').click(function() {
        var customID = $(this).attr('data-id');
        $.get('/chat/server/', {
            'customID': customID,
        }, function(data) {
            $('.message-box').empty();
            $('.message-box').append(data);
        }, 'html');
        $('.server-dashboard').slideDown(500);
    });

    $('#send-message').click(function() {
        var content = $('.message-input').find('[name="content"]').val();
        var customID = $('.message-box').find('input[name="customID"]').val();
        if (content == '' || customID == '') {
            return;
        }
        $.post('/chat/new/server/', {
            'content': content,
            'customID': customID,
        }, function(data) {
            if (data['success']) {
                $('.message-box').append('<p class="leftMessage">' + content + '</p>');
                $('.message-input').find('[name="content"]').val('');
            } else {
                alert(data['wrong']);
            }
        }, 'json');
    });

    $(document).keypress(function(event) {
        if (event.which == 13) {
            var content = $('.message-input').find('[name="content"]').val();
            var customID = $('.message-box').find('input[name="customID"]').val();
            if (content == '' || customID == '') {
                return;
            }
            $.post('/chat/new/server/', {
                'content': content,
                'customID': customID,
            }, function(data) {
                if (data['success']) {
                    $('.message-box').append('<p class="leftMessage">' + content + '</p>');
                    $('.message-input').find('[name="content"]').val('');
                } else {
                    alert(data['wrong']);
                }
            }, 'json');
        }
    });

    function getNewMessage() {
        var customID = $('.message-box').find('input[name="customID"]').val();
        if (!customID) {
            return;
        }
        $.get('/chat/get/server/', {
            'customID': customID,
        }, function(data) {
            $('.message-box').append(data);
        }, 'html');
    }

    function getCustomList() {
        $.get('/chat/session/', {
        }, function(data) {
            $('.custom-session').empty();
            $('.custom-session').append(data);
            if (toggle == 0) {
                $('.button-item').show();
            }
            $('.button-item').click(function() {
                var customID = $(this).attr('data-id');
                $.get('/chat/server/', {
                    'customID': customID,
                }, function(data) {
                    $('.message-box').empty();
                    $('.message-box').append(data);
                }, 'html');
                $('.server-dashboard').slideDown(500);
            });
        }, 'html');
    }

    setInterval(getCustomList, 2000);
    setInterval(getNewMessage, 1000);
});