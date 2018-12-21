config = {
    "title": "Coupled Pattern Learner",
    "lib": {
        "css": [
            #"public/node_modules/bootstrap/dist/css/bootstrap.css",
            "public/node_modules/materialize-css/dist/css/materialize.min.css",
            "public/node_modules/font-awesome/css/font-awesome.css",
        ],
        "js": [
            "public/node_modules/materialize-css/dist/js/materialize.min.js",
            "public/node_modules/jquery/dist/jquery.js",
            "public/node_modules/popper.js/dist/popper.js",
            "public/node_modules/bootstrap/dist/js/bootstrap.js",
            "public/node_modules/angular/angular.js",
            "public/node_modules/angular-ui-router/release/angular-ui-router.js",
            "public/node_modules/angular-resource/angular-resource.js",
            "public/node_modules/angular-animate/angular-animate.js",
            "public/node_modules/angular-aria/angular-aria.js",
            "public/node_modules/angular-messages/angular-messages.js"
        ]
    },
    "css": [
        "modules/*/css/*.css"
    ],
    "js": [
        "modules/core/app/config.js",
        "modules/core/app/init.js",
        "modules/**/*.js",
        "modules/*/controller/*.js",
        "modules/*/routes/*.js",
        "modules/*/services/*.js"
    ],
    "views": [
         "modules/*/views/*.html"
    ]
}