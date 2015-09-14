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
        console.log($location.path())
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
    console.log("Enetered........................");


});

app.controller('LoginPageController',function($scope, $location, $http, $sce){
            //console.log("hiiiiiiiiiiiiiiiiiiiiiiiiiiii")

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

                console.log("Success")
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
        console.log("jshjdhsjdh")
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

                console.log("Success")
                $window.location.href = '#signup/step2';

            }).
            error(function (data, status, headers, config) {
                alert("Error")
                console.log("Error123");
            });
                               }


});

app.controller('SignUpPage2Controller', function($scope, $location,$http,$window) {
    jQuery("body").removeClass("home");
    console.log("*********************************")

    $http.get("/api/v1/profile/update/").then(function(result) {
     $scope.currentUser = result.data.user;
        console.log("00000000000000",result.data.user.id)
  })

    $scope.data = [{'name':'Chris', 'email':''} ]

    $scope.addNewChild = function(){
                 $scope.data.push({'question': "", id: "", 'answer': ""});
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
            console.log("shdgshdghsgdhjsgdksghdksgd", childname,age,gender1)

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
                console.log("Errorsssssss")
            })

    }
});







