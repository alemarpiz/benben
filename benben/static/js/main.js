// Require.js allows us to configure shortcut alias
// Their usage will become more apparent futher along in the tutorial.
require.config({
  baseUrl: 'static/js',
  paths: {
    // Major libraries
    lodash: 'libs/lodash',
    backbone: 'libs/backbone',
    marionette: 'libs/backbone.marionette',
    bootstrap: '../bootstrap/js/bootstrap',

    // Require.js plugins
    text: 'libs/require/text'

  },

  shim: {
    lodash: {
      exports: '_'
    },
    backbone : {
      deps: ['jquery', 'lodash'],
      exports: 'Backbone'
    },
    marionette: {
      deps: ['jquery', 'lodash', 'backbone'],
      exports: 'Marionette'
    }
  }

});

// Let's kick off the application

require([
  'jquery',
  'lodash',
  'backbone',
  'marionette'
], function($, _, Backbone, Marionette){
  
  var VoodooDoll = Backbone.Model.extend({
    defaults: {
      name: 'James Taylor'
    }
  });

  var voo = new VoodooDoll();

  $('body').prepend(voo.get('name'));
});
