$(document).on('click', '.user-menu-trigger', function (e) {
   e.stopPropagation();
   $('.user-menu-drop').toggle();
});

$(document).click(function() {
   $('.user-menu-drop').hide();
});