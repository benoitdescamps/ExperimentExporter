var myApp = angular.module('myApp',['infinite-scroll']);
myApp.controller('DataController', function($scope,$http) {
   $http.get("/s/").then(function(r) {
                    $scope.data = r.data;
            });
   $scope.onMouseOver = function(user){
        console.log("mouse over user: " + user.message_id)
    }

});