//router
app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    when('/about', {
        templateUrl: '/static/js/angular/templates/about.html',
        controller: 'aboutPageController'
  }).when('/', {
            redirectTo: '/'
        })


  }]);

