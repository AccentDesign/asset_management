$(document).on('click', '.menu', function (e) {
   e.stopPropagation();
   $(this).find('.menu-drop').toggle();
});

$(document).click(function() {
   $('.menu-drop').hide();
});

$(document).on('click', '.alert .close', function (e) {
   e.preventDefault();
   $(this).closest('.alert').hide();
});
