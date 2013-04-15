define([
    'backbone',
    'app',
    // Views
    'views/hero',
    'views/row',
    // Models
    'models/row'
], function(Backbone, app, HeroView, RowView, Row) {

    var TypeResolver = function() {
        this.view_mapping = {
            'hero': HeroView,
            'row': RowView
        };
        this.model_mapping = {
            'row': Row
        };
    };
    _.extend(TypeResolver.prototype, {
        getModel: function(type) {
            var model;
            
            model = this.model_mapping[type];

            if (!model) model = Backbone.Model;
            
            return model;
        },
        getView: function(type) {
            var view;
            
            view = this.view_mapping[type];

            if (!view) {
                throw('No view defined for this type.', 'NoItemTypeViewError');
            }
            
            return view;
        }
    });

    return  new TypeResolver();
});