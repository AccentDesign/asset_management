$.fn.treetable = function(options) {

    var _this = this;

    var settings = $.extend({
        nodeIconSelector: '.node-icon',
        toggleAllSelector: '.toggle-all',
        collapsedIconCls: 'icon-plus-squared-alt',
        expandedIconCls: 'icon-minus-squared-alt'
    }, options);

    function toggleNode(node) {
        // toggle the children of a node
        var tr = $('[data-node="' + node + '"]');
        var icon = $(tr).find(settings.nodeIconSelector);

        if (icon.hasClass(settings.collapsedIconCls)) {
            icon.removeClass(settings.collapsedIconCls);
            icon.addClass(settings.expandedIconCls);
        } else {
            icon.removeClass(settings.expandedIconCls);
            icon.addClass(settings.collapsedIconCls);
        }

        var children = $(_this).find('[data-parent-node="' + node + '"]');

        $.each(children, function () {
            if ($(this).hasClass('d-hidden')) {
                $(this).removeClass('d-hidden');
            } else {
                $(this).addClass('d-hidden');
                hideChildNodes($(this).data('node'));
            }
        });
    }

    function hideChildNodes(node) {
        // hide entire tree under a single node
        var tr = $('[data-node="' + node + '"]');
        var icon = $(tr).find(settings.nodeIconSelector);

        icon.removeClass(settings.expandedIconCls);
        icon.addClass(settings.collapsedIconCls);

        var children = $(_this).find('[data-parent-node="' + node + '"]');

        $.each(children, function () {
            $(this).addClass('d-hidden');
            hideChildNodes($(this).data('node'));
        });
    }

    function hideAllNodes() {
        // hide all rows except for the root nodes
        var trs = $('[data-node]');
        $.each(trs, function () {
            if ($(this).data('parent-node')) {
                $(this).addClass('d-hidden');
            }
            var icon = $(this).find(settings.nodeIconSelector);
            icon.removeClass(settings.expandedIconCls);
            icon.addClass(settings.collapsedIconCls);
        });
    }

    function showAllNodes() {
        // show all nodes
        var trs = $('[data-node]');
        $.each(trs, function () {
            $(this).removeClass('d-hidden');
            var icon = $(this).find(settings.nodeIconSelector);
            icon.removeClass(settings.collapsedIconCls);
            icon.addClass(settings.expandedIconCls);
        });
    }

    $(_this).on('click', '[data-node]', function () {
        var node = $(this).data('node');
        toggleNode(node);
    });

    $(_this).on('click', settings.toggleAllSelector, function () {
        if ($(_this).find('[data-node].d-hidden').length > 0) {
            showAllNodes();
        } else {
            hideAllNodes();
        }
    });

    $(_this).on('click', 'a[href]' , function (e) {
        // stop links toggling tree
        e.stopPropagation()
    });

    return _this;

};