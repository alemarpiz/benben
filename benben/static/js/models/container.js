define([
    'backbone',
    'collections/sections'
], function(Backbone, SectionCollection) {

    var ContainerModel = Backbone.Model.extend({
        defaults: {
            'sections': new SectionCollection()
        },
        parse: function(response) {
            if (response.sections !== undefined) {
                response.sections = new SectionCollection(response.sections);
            }
            return response;
        },
        set: function(attributes, options) {
            if (attributes.sections !== undefined && !(attributes.sections instanceof SectionCollection)) {
                attributes.sections = new SectionCollection(attributes.sections);
            }
            return Backbone.Model.prototype.set.call(this, attributes, options);
        }
    });

    return ContainerModel;
});