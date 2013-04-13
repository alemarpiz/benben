// Require.js allows us to configure shortcut alias
// Their usage will become more apparent futher along in the tutorial.
require.config({
  baseUrl: 'static/js',
  paths: {
    // Major libraries
    jquery: '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    lodash: 'libs/lodash',
    backbone: 'libs/backbone',
    marionette: 'libs/backbone.marionette',

    // Require.js plugins
    text: 'libs/require/text'

  },

  shim : {
    jquery : {
      exports : 'jQuery'
    },
    lodash : {
      exports : '_'
    },
    backbone : {
      deps : ['jquery', 'lodash'],
      exports : 'Backbone'
    },
    marionette : {
      deps : ['jquery', 'lodash', 'backbone'],
      exports : 'Marionette'
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
