define([
    'marionette',
    'lodash',
    'app',
    'text!templates/hero.html'
], function(Marionette, _, app, HeroTemplate){

    var HeroView = Backbone.Marionette.ItemView.extend({
        template: _.template(HeroTemplate)
    });

    return HeroView;

});