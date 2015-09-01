app.controller('mainController', function($scope, $location){

    $scope.redirectToHome= function () {
        window.location.href = '/';
        $location.path('/'); };

});

app.controller('aboutPageController', function($scope, $location) {

    var main_div = angular.element( document.querySelector( '#above-the-fold' ) );
    main_div.remove();
    jQuery("body").removeClass("home");

});
