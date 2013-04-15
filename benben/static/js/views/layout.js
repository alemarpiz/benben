define([
    'jquery',
    'backbone',
    'marionette',
    'types',
    'views/row',
    'collections/sections'
], function($, Backbone, Marionette, types, RowView, SectionCollection){

    var LayoutView = Backbone.Marionette.CollectionView.extend({

        initialize: function() {
            var layout = this.options.layout;
            if (layout) {
                this.collection = new SectionCollection();
                this.collection.add(layout.sections);
            }
        },

        getItemView: function(item) {
            var itemView, type;

            type = item.get('view') ? item.get('view') : item.get('type');
            if (type) {
                itemView = types.getView(type);
            }

            if (!itemView){
                throwError("View lookup failed.", "ViewLookupError");
            }

            return itemView;
        }
    });

    return LayoutView;

});