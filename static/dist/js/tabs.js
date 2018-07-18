$.fn.tabs = function (options) {

    /**
     * usage:
     *
     * <ul class="tabs">
     *     <li data-tab-id="tab1" class="active"><a>Tab 1</a></li>
     *     <li data-tab-id="tab2"><a>Tab 2</a></li>
     * </ul>
     * <div data-tab="tab1"></div>
     * <div data-tab="tab2" class="d-hidden"></div>
     *
     */

    var _this = this;

    var settings = $.extend({
        tabActiveCls: 'active',
        tabErrorCls: 'error',
        panelHiddenCls: 'd-hidden',
        panelErrorSelector: '.errorlist'
    }, options);

    $(_this).on('click', 'li', function () {

        // switch tabs

        var tabId = $(this).data('tab-id');

        // deactivate tabs
        $(this).siblings().each(function () {
            $(this).removeClass(settings.tabActiveCls);
        });

        // activate clicked tab
        $(this).addClass(settings.tabActiveCls);

        // hide all data-tab elements
        $('[data-tab]').each(function () {
            $(this).addClass(settings.panelHiddenCls);
        });

        // show selected data-tab element
        $('[data-tab="' + tabId + '"]').removeClass(settings.panelHiddenCls);

    });

    $(_this).find('li').each(function () {

        // look in each data-tab for the form errors and add the error class to the
        // tab if any are found

        var tabId = $(this).data('tab-id');
        var hasError = $('[data-tab="' + tabId + '"]').find(settings.panelErrorSelector).length > 0;

        if (hasError) {
            $(this).addClass(settings.tabErrorCls);
        } else {
            $(this).removeClass(settings.tabErrorCls);
        }

    });

    return _this;

};
