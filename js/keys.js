
// scroll-to-top animate
$(document).ready(function() { 
    jQuery('.entry_date_published').click(function(){
        jQuery("html, body").animate({ scrollTop: 0 }, 600);
            return false;
    });
});

/*
//console.log($('#menu').contents().find('.menu_link').html()); //.addClass('feed_active');

var doc = window.frames['iframe.menu'].document;
$(doc).ready(function(){
    $('body').prepend('This is outside the iframe<br>');
    $('body',doc).prepend('This is inside the iframe<br>');

    $('body', doc).delegate('*', 'hover', function() {
        $(this).addClass('blablabla');
        $(this).css('textDecoration', 'underline');
    });
});


document.addEventListener('keydown', function(event) {
    var feed_active = $('iframe#menu').contents().find('.feed_active');
    console.log('>>>>>> '+feed_active.html());
    var feed_active_next = $('iframe#menu').contents().find('.feed_active').next('div').addClass('feed_active');
    console.log('>>>>>> '+feed_active_next.html());


    // Binding for 'n', select next feed
    if ((event.keyCode == 78) && (feed_active.next().length != 0)) {
        console.log('up');
        var feed_active = $('iframe#menu').contents().find('.feed_active').removeClass('feed_active');
        feed_active = $('iframe#menu').contents().find('.feed_active').next('div').addClass('feed_active');
        console.log('up'+ feed_active.html());
    }
    else if ((event.keyCode == 80) && (feed_active.prev().length != 0)) {
        console.log('down');
        var feed_active = $('iframe#menu').contents().find('.feed_active').removeClass('feed_active');
        feed_active = $('iframe#menu').contents().find('.feed_active').prev('div').addClass('feed_active');
        console.log('down'+ feed_active.html());
    }
});



// Add '.active' to first div with class '.entry_box'
$('.entry_box:first').addClass('entry_active');

document.addEventListener('keydown', function(event) {
    var entry_active = $('div.entry_active');

    // Binding for 'j', previous entry
    if ((event.keyCode == 74) && (entry_active.next('div').length != 0)) {
        var entry_active = $('div.entry_active').removeClass('entry_active');
        var position = $(entry_active).next('div').position();
        scroll(0,position.top);
        $(entry_active).next('div').addClass('entry_active');
        console.log('selected next entry');
    }
    // Binding for 'k', next entry
    else if ((event.keyCode == 75) && (entry_active.prev('div').length != 0)) {
        var entry_active = $('div.entry_active').removeClass('entry_active');
        var position = $(entry_active).prev('div').position();
        scroll(0,position.top);
        $(entry_active).prev('div').addClass('entry_active');
        console.log('selected previous entry');
    }
});
*/
