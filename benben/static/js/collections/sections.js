define([
    'backbone',
    'types'
], function(Backbone, types) {
    var SectionCollection = Backbone.Collection.extend({
        model: function(attrs, options) {
            var type, model;
            if (attrs.type) {
                type = attrs.type;
            } else {
                type = 'default';
            }
            model = types.getModel(type);
            return new model(attrs, options);
        }
    });
    return SectionCollection;
});