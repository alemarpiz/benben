define([
    'marionette',
    'views/layout'
], function(Marionette, LayoutView){

    var RowView = LayoutView.extend({
        className: 'row-fluid'
    });

    return RowView;

});