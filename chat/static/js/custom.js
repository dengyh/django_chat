$(function() {
    var visible = false;
    $('.button-background').click(function() {
        $('.custom-dashboard').slideToggle(500);
        $('.button-tip').fadeOut(500);
        visible = visible ^ true;
    });

    $('#send-message').click(function() {
        var content = $('.message-input').find('[name="content"]').val();
        if (!content) {
            return;
        }
        $.post('/chat/new/custom/', {
            'content': content,
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
            if (!content) {
                return;
            }
            $.post('/chat/new/custom/', {
                'content': content,
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

    $('#contact-form').submit(function() {
        var name = $(this).find('[name="name"]').val();
        var phone = $(this).find('[name="phone"]').val();
        $.post('/chat/custom/', {
            'name': name,
            'phone': phone,
        }, function(data) {
            $('.custom-dashboard').empty();
            $('.custom-dashboard').append(data);
            $('#send-message').click(function() {
                var content = $('.message-input').find('[name="content"]').val();
                if (!content) {
                    return;
                }
                $.post('/chat/new/custom/', {
                    'content': content,
                }, function(data) {
                    if (data['success']) {
                        $('.message-box').append('<p class="leftMessage">' + content + '</p>');
                        $('.message-input').find('[name="content"]').val('');
                    } else {
                        alert(data['wrong']);
                    }
                }, 'json');
            });
        }, 'html');
        return false;
    });

    function getNewMessage() {
        var id = $('.custom-dashboard').find('[name="id"]').val();
        if (!id) {
            return;
        }
        $.get('/chat/get/custom/', {}, function(data) {
            if (data != '') {
                $('.message-box').append(data);
                if (!visible) {
                    $('.button-tip').fadeIn(500);
                }
            }
        }, 'html');
    }

    setInterval(getNewMessage, 1000);
});