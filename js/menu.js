$(document).ready(function(){
    $(".menu div.menu_group_title").click(function() {
        if ($(this).siblings().is(":hidden")) {
            $(this).siblings().slideDown();
            $.cookie($(this).parent().get(0).className, 'true', {expires: 30, path:'/'});
        }
        else {
            $(this).siblings().slideUp();
            $.cookie($(this).parent().get(0).className, 'false', {expires: 30, path:'/'});
        }
    });
    // Restore state from cookie
    $(".menu div.menu_group_title").each(function() {
        var c = $.cookie($(this).parent().get(0).className);
        if (c == 'true') { $(this).siblings().show(); }
        else if (c == 'false') { $(this).siblings().hide(); }
        else { $(this).siblings().hide(); }
    });
});
