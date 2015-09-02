//router
app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    when('/about', {
        templateUrl: '/static/js/angular/templates/about.html',
        controller: 'aboutPageController'
  }).
        when('/parents', {
        templateUrl: '/static/js/angular/templates/parents.html',
        controller: 'aboutPageController'
  }).
        when('/teach', {
        templateUrl: '/static/js/angular/templates/teach.html',
        controller: 'aboutPageController'
  }).
        when('/', {
            url: '/home'
        })


  }]);



