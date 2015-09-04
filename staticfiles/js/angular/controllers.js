app.controller('mainController', function($scope, $location, $http, $sce){

        $http({ method: 'GET', url: '/api/v1/get_home_page' }).
            success(function (data, status, headers, config) {

                jQuery("body").addClass("home");
                $scope.page = $sce.trustAsHtml(data);


            }).
            error(function (data, status, headers, config) {
                alert("failed");
            });

});

app.controller('CommonPageController', function($scope, $location) {


    jQuery("body").removeClass("home");

});


app.controller('HomePageController', function($scope, $location, $http) {


    jQuery("#remove-this-id").hide();
    jQuery("body").addClass("home");

});


