$(document).on('click', '.user-menu-trigger', function (e) {
   e.stopPropagation();
   $('.user-menu-drop').toggle();
});

$(document).click(function() {
   $('.user-menu-drop').hide();
});

$(document).on('click', '.alert .close', function (e) {
   e.preventDefault();
   $(this).closest('.alert').hide();
});
