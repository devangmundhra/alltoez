var cities = [
    {
        city : 'Toronto',
        desc : 'This is the best city in the world!',
        lat : 43.7000,
        long : -79.4000
    },
    {
        city : 'New York',
        desc : 'This city is aiiiiite!',
        lat : 40.6700,
        long : -73.9400
    },
    {
        city : 'Chicago',
        desc : 'This is the second best city in the world!',
        lat : 41.8819,
        long : -87.6278
    },
    {
        city : 'Los Angeles',
        desc : 'This city is live!',
        lat : 34.0500,
        long : -118.2500
    },
    {
        city : 'Las Vegas',
        desc : 'Sin City...\'nuff said!',
        lat : 36.0800,
        long : -115.1522
    }
];

var event={};
var count;

app.controller('mainController', function($scope, $location, $http, $sce){
    if($location.path()=='/') {
        $http({ method: 'GET', url: '/api/v1/get_home_page' }).
            success(function (data, status, headers, config) {

                jQuery("body").addClass("home");
                $scope.page = $sce.trustAsHtml(data);


            }).
            error(function (data, status, headers, config) {
                //handle error here if needed
            });
    }
    else if($location.path()=='/login'){
        $scope.user = {};
        jQuery("body").removeClass("home");
        $http({ method: 'GET', url: '/api/v1/get_login_page' }).
            success(function (data, status, headers, config) {

                $scope.login_page = $sce.trustAsHtml(data);


            }).
            error(function (data, status, headers, config) {
                //handle error here if needed
            });
        jQuery("#login-button").attr('ng-click', 'login()');
    }


});

app.controller('CommonPageController', function($scope, $location) {
    jQuery("body").removeClass("home");
});


app.controller('HomePageController', function($scope, $location, $http) {
    jQuery("body").addClass("home");
});

app.controller('LoginViewController', function($scope, $location, $http) {
    jQuery("body").removeClass("home");
});

app.controller('LoginFormController',function($scope, $http, $state){

});

app.controller('LoginPageController',function($scope, $location, $http, $sce){


    $http({ method: 'GET', url: '/api/v1/get_login_page' }).
            success(function (data, status, headers, config) {

                $scope.facebookPage = $sce.trustAsHtml(data);
            }).
            error(function (data, status, headers, config) {
                //handle error here if needed
            });

            jQuery("body").removeClass("home");
});

app.controller('LoginFormController', function($scope, $http, $location,$window){

     $scope.user = {};
    $scope.login = function(){
        $scope.user = {};
        username = $("#Username").val()
        password = $("#Password").val()
        data = {
                'username': username,
                'password': password
            }

        $http({ method: 'POST', url: '/api/v1/login/',
            data: data
        }).
            success(function (data, status, headers, config) {
                $window.location.href = '#events';
            }).
            error(function (data, status, headers, config) {
                console.log("Error");
            });
                               }


});

app.controller('SignupPageController',function($scope,$http,$location,$sce){
    $http({method:'GET',url:'/api/v1/get_login_page'}).
        success(function(data, status, headers, config){
        $scope.facebookSignup = $sce.trustAsHtml(data);
    }).
        error(function(data,status,headers,config){
            console.log("Error")
        });
});

app.controller('SignUpFormController', function($scope, $http, $location,$window){
        $scope.signup1 = function(){
        username = $("#Username").val()
        password = $("#Password").val()
        data = {
                'username': username,
                'password': password
            }

        $http({ method: 'POST', url: '/api/v1/signup/',
            data: data
        }).
            success(function (data, status, headers, config) {
                $window.location.href = '#signup/step2';

            }).
            error(function (data, status, headers, config) {
            });
                               }



});

app.controller('SignUpPage2Controller', function($scope, $location,$http,$window) {
    jQuery("body").removeClass("home");

    $http.get("/api/v1/profile/update/").then(function(result) {
     $scope.currentUser = result.data.user;
  })

    $scope.data = [{'name':'', 'email':''} ]

    $scope.addNewChild = function(){
                 $scope.data.push({'name': "", 'age': "", 'gender': ""});
               };

    console.log("Next step is to save")


    $scope.update = function() {
            first_name = $ ("#id_first_name").val()
            last_name = $ ("#id_last_name").val()
            gender    = $("#gender").val()
            zipcode = $("#id_zip_code").val()
            city_name = $("#id_city_name").val()
            state_anme = $("#id_state_name").val()
            console.log("**********",first_name,last_name,gender,zipcode,city_name,state_anme)
            childname = $("#id_child").val()
            age = $("#id_age").val()
            gender1 =$("#gender1").val()
            console.log("@@@@@@@@@@@@@@@@@@@@@@", childname,age,gender1)

        data = {
                'user' : $scope.currentUser,
                'gender': gender,
                'zipcode': zipcode,
                'city'  : city_name,
                'state' : state_anme,
                'first_name': first_name,
                'last_name' : last_name
            }
        $http({ method:'PUT', url: '/api/v1/profile/update/',data: data
        }).
            success(function(data,status){

                console.log("Success")
            }).
            error(function(data,status){
                console.log("Error")
            });

        datas = {'children': [{
            'user'    :  $scope.currentUser,
               'name'   : childname,
            'gender'    : gender1,
                'age'   : age}
        ]}



        $http({ method:'POST',url:'/api/v1/child/',data:datas}).
            success(function(data,status){
                console.log("Success")
            }).
            error(function(data,status){
                console.log("Error")
            })

    }
});


app.controller("EventController",function($scope,$http,$location){
    jQuery("body").removeClass("home");
    $scope.is_pagination_request_fired = false


        $scope.getEvents = function(url, type) {
            if(!url && type){
                url = '/api/v1/order/?ordering='
            }
            if(type){
                url = url + type
            }
            console.log(url)
            $http({ method: 'GET', url: url}).

                success(function (data, status) {
                    count = data.count;
                    event = data.results;
                    $scope.events = data.results;
                    console.log(data.results[0].venue.latitude, data.results[0].venue.longitude, data.results[0].venue.name,data.results[0].description)
                    $scope.counts = data.count;
                    $scope.next_url_params = data.next;
                    $scope.pagination = $scope.pagination.concat(data.results);

                }).

                error(function (data, status) {
                    console.log("Failed");
                })
        }

        $scope.PageNext = function() {

            if('next_url_params' in $scope){
                    next_url_params = $scope.next_url_params
                } else{
                    next_url_params = '/api/v1/events/'
                    $scope.pagination = []
                }
            $scope.getEvents(next_url_params, '');
    }

});


app.controller("EventDetailController",function($scope,$http,$location){

    console.log("Entered in  to Event Controller");

    var url = $location.path().split( '/detail/' );
    console.log(url);
    var regex = new RegExp(/([0-9]+)/);
    var match = regex.exec(url);
    $scope.event_id =  match[1];
    new_url = '/api/v1/detail/?q=' + $scope.event_id

    jQuery("body").removeClass("home");

    $http({ method:'GET',url: new_url}).

    success(function(data,status){

        $scope.event = data.results[0];
    }).

    error(function(data,status){
        console.log("Failed");
    })

});

app.controller("CategoryController",function($scope,$http,$location){
    console.log("Entered in to Category Controller");

    jQuery("body").removeClass("home");

    var url = $location.path().split('/events/category/');
    console.log("Location Path:", url[1]);
    new_url = '/api/v1/sort/?q=' + url[1]

    $scope.PageNext = function() {


            if('next_url_params' in $scope){
                    next_url_params = $scope.next_url_params
                } else{
                    next_url_params = new_url;
                    $scope.pagination = []
                }


        $http({ method: 'GET', url: next_url_params}).

            success(function (data, status) {
                console.log("count", data.count);
                $scope.events = data.results;
                $scope.counts = data.count;
                $scope.next_url_params = data.next;
                $scope.pagination = $scope.pagination.concat(data.results);

            }).

            error(function (data, status) {
                console.log("Failed");
            })

    }



})

app.controller("GoogleMapController", function($scope,$location,$http){

    console.log("Entered in to Google Map Controller");

    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(40.0000, -98.0000),
        mapTypeId: google.maps.MapTypeId.TERRAIN
    }

    $scope.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    $scope.markers = [];

var infoWindow = new google.maps.InfoWindow();

    var createMarker = function (info) {

        var marker = new google.maps.Marker({
            map: $scope.map,
            position: new google.maps.LatLng(info.lat, info.long),
            title: info.city
        });
        marker.content = '<div class="infoWindowContent">' + info.desc + '</div>';

    google.maps.event.addListener(marker, 'click', function(){
            infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
            infoWindow.open($scope.map, marker);
        });

        $scope.markers.push(marker);

    }

    for (i = 0; i < cities.length; i++){
        createMarker(cities[i]);
    }

    $scope.openInfoWindow = function(e, selectedMarker){
        e.preventDefault();
        google.maps.event.trigger(selectedMarker, 'click');
    }


})


var cities = [
    {
        city : 'Toronto',
        desc : 'This is the best city in the world!',
        lat : 43.7000,
        long : -79.4000
    },
    {
        city : 'New York',
        desc : 'This city is aiiiiite!',
        lat : 40.6700,
        long : -73.9400
    },
    {
        city : 'Chicago',
        desc : 'This is the second best city in the world!',
        lat : 41.8819,
        long : -87.6278
    },
    {
        city : 'Los Angeles',
        desc : 'This city is live!',
        lat : 34.0500,
        long : -118.2500
    },
    {
        city : 'Las Vegas',
        desc : 'Sin City...\'nuff said!',
        lat : 36.0800,
        long : -115.1522
    }
];

var event={};
var count;
console.log(data.results[0].venue.latitude,"@@@@@@@@@@@@", data.results[0].venue.longitude, data.results[0].venue.name,data.results[0].description)


for (i=0;i<count;i++)
{
    var cities = [

    ]

}













