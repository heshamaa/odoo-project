odoo.define('construction_management.CategoryTreeWidget', [
    'web.ListRenderer',
    'web.field_registry',
], function(ListRenderer, fieldRegistry) {
    "use strict";

    var CategoryTreeRenderer = ListRenderer.extend({
        _renderBody: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {

                function renderRow($row, level) {
                    var $tds = $row.find('td');
                    // Padding حسب المستوى
                    $tds.eq(0).css({
                        'padding-left': (level * 25) + 'px',
                        'font-weight': level === 0 ? 'bold' : 'normal',
                        'background-color': level === 0 ? '#f0f0f0' : 'transparent'
                    });
                }

                // نعمل loop على كل الصفوف
                self.$el.find('tr').each(function() {
                    var $row = $(this);
                    var level = parseInt($row.data('level') || 0);

                    // تطبيق الـ hierarchy styling
                    renderRow($row, level);
                });
            });
        },
    });

    fieldRegistry.add('category_tree_widget', CategoryTreeRenderer);
});
