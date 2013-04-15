define([
    'marionette',
    'lodash'
], function(Marionette, _){

    var BenbenApp = Backbone.Marionette.Application.extend({});

    var app = new BenbenApp();

    app.addRegions({
        main: '#app_region'
    });

    return app;
});