app.controller('mainController', function($scope, $location, $http){

    $scope.redirectToHome= function () {
        window.location.href = '/';
        $location.path('/'); };

});

app.controller('CommonPageController', function($scope, $location) {


//    var main_div = angular.element( document.querySelector( '#remove-this-id' ) );
//    main_div.remove();
    jQuery("#remove-this-id").hide()
    jQuery("body").removeClass("home");
    console.log('In new router state');

});


app.controller('HomePageController', function($scope, $location, $http) {


    jQuery("#remove-this-id").hide();
    jQuery("body").addClass("home");

});


