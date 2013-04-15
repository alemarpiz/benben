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
    'app',
    'types',
    'views/layout'
], function(BenbenApp, types, LayoutView) {
    
    var schema = {
        sections: [
            {
                type: 'hero',
                title: 'Welcome to Benben!',
                description: 'Benben is a Layout Management System or LMS.'
            },
            {
                type: 'row',
                sections: [
                    {
                        width: 4,
                        sections: [
                            {
                                type: 'simple',
                                content: '<h2>Some Content</h2>'
                            }
                        ]
                    },
                    {
                        width: 4,
                        sections: [
                            {
                                type: 'simple',
                                content: '<h2>Some More</h2>'
                            }
                        ]
                    },
                    {
                        width: 4,
                        sections: [
                            {
                                type: 'simple',
                                content: '<h2>Some Content</h2>'
                            }
                        ]
                    }
                ]
            },
            {   
                type: 'row',
                columns: [
                    {
                        width: 6
                    },
                    {
                        width: 3
                    },
                    {
                        width: 2
                    }
                ]
            }
        ]
    };

    var layout = new LayoutView({
        layout: schema
    });

    BenbenApp.main.show(layout);

});
