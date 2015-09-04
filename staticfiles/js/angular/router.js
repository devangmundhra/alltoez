//router
app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    when('/', {
        templateUrl: '/static/js/angular/templates/home.html',
        controller: 'mainController'
  }).when('/about', {
        templateUrl: '/static/js/angular/templates/about.html',
        controller: 'CommonPageController'
  }).
        when('/parents', {
        templateUrl: '/static/js/angular/templates/parents.html',
        controller: 'CommonPageController'
  }).
        when('/teach', {
        templateUrl: '/static/js/angular/templates/teach.html',
        controller: 'CommonPageController'
  })


  }]);



