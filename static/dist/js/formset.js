$.fn.formset = function (options) {

    /**
     * usage:
     */

    var _this = this;
    var prefix = $(_this).data('formset-prefix');

    var settings = $.extend({
        formsetAddSelector: '.formset-add',
        formsetDeleteSelector: 'input[id*="-DELETE"]',
        formsetCls: 'formset',
        emptyCls: 'formset-empty',
        deletedCls: 'formset-deleted'
    }, options);

    $(_this).on('click', settings.formsetAddSelector, function(){
        var $original = $(_this).find('.' + settings.emptyCls);
        var $copy = $($original).clone(true, true);

        $($copy).removeClass(settings.emptyCls);
        $($copy).addClass(settings.formsetCls);

        var $total = $('#id_' + prefix + '-TOTAL_FORMS').val();
        $($copy).html( $($copy).html().replace(/__prefix__/g, $total) );

        $total++;

        $('#id_' + prefix + '-TOTAL_FORMS').val($total);

        $($original).before($copy);
    });

    $(_this).on('change', settings.formsetDeleteSelector, function () {
        if ($(this).is(':checked')) {
            $(this).closest('.' + settings.formCls).addClass(settings.deletedCls);
        } else {
            $(this).closest('.' + settings.formCls).removeClass(settings.deletedCls);
        }
    });

    return _this;

};
