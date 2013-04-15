define([
    'backbone',
    'models/container'
], function(Backbone, Container){

    var Row = Container.extend({
        initialize: function() {
            this.get('sections').on('add', function(model) {
                this.validate();
            }, this);
        },
        validate: function() {
            var sections, width;

            sections = this.get('sections');
            if (sections.length > 0) {
                sections.each(function(model) {
                    if (!model.get('width')) {
                        throw('Sections inside of a Row require a `width`.', 'InvalidWidthError');
                    } else {
                        width += model.get('width');
                    }
                }, this);
                if (width > 12) {
                    throw('Total sum of section widths inside of Rows cannot exceed 12.', 'InvalidWidthError');
                }
            }
        }
    });

    return Row;

});