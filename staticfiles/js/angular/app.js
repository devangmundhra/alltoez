var app = angular.module('app', ['ngRoute', ]);

    // HTTP requests need to be considered AJAX requests.
app.config(["$httpProvider", function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
    $httpProvider.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
}]);