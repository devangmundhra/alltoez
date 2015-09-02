app.controller('mainController', function($scope, $location){

    $scope.redirectToHome= function () {
        window.location.href = '/';
        $location.path('/'); };

});

app.controller('aboutPageController', function($scope, $location) {


    var main_div = angular.element( document.querySelector( '#remove-this-id' ) );
    main_div.remove();
    jQuery("body").removeClass("home");
    console.log('In new router state');

});
