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
  }).
      when('/login',{
          templateUrl:'/static/js/angular/templates/login_register.html',
          controller:'LoginPageController'
   }).
        when('/signup',{
            templateUrl:'/static/js/angular/templates/signup.html',
            controller:'SignupPageController'
   }).
        when('/signup/step2',{
            templateUrl: '/static/js/angular/templates/signup_step2.html',
            controller: 'SignUpPage2Controller'
   }).
            when('/child',{
            templateUrl:'/static/js/angular/templates/teach.html',
            controller: 'ChildController'
   }).

        when('/events',{
            templateUrl:'/static/js/angular/templates/event_list_page.html',
            controller : 'EventController'
   }).
      when('/detail/:slug/:event_id',{
          templateUrl:'/static/js/angular/templates/event_detail_page.html',
          controller: 'EventDetailController'

   }).
       when('/events/category/:slug',{
            templateUrl:'/static/js/angular/templates/event_list_page.html',
            controller: 'CategoryController'
        })


  }]);







