var myApp = angular.module('myApp',['infinite-scroll']);
myApp.controller('DataController', function($scope,$http) {
   $http.get("/s/").then(function(r) {
                    $scope.data = r.data.unknown_emails;
                    $scope.data_main = r.data.unknown_emails;
                    $scope.data_class0 = [$scope.data[0]];
                    $scope.data_class1 = [$scope.data[1]];
            });
   $scope.onMouseOver = function(user){
        console.log("mouse over user: " + user.message_id)


        $scope.eFrom = user.header_from;
        $scope.eSent = user.header_date;
        $scope.eTo = user.header_to;
        $scope.eSubject = user.header_subject;
        $scope.eContent = user.email_body;
    }

   $scope.onChangeClass0 = function(user){
        user.class1 = !user.class0}
   $scope.onChangeClass1 = function(user){
        user.class0 = !user.class1}

   $scope.onSubmit = function(user) {
        console.log("Checked box of user id: " + user.message_id);

        if(user.pred_class0)
            console.log("Added to class 0: " + user.message_id)
            $scope.data_class0.push(user);
        if(user.pred_class1)
            console.log("Added to class 1: " + user.message_id)
            $scope.data_class1.push(user);
        $http({
            method : 'POST',
            url : '/',
            data : angular.copy(user)
        });



    };

       $scope.onSelectTab_main = function() {
        console.log("New Tab Selected: ");
        $scope.data = $scope.data_main;
    };
       $scope.onSelectTab_class0 = function() {
        console.log("New Tab Selected: ");
        $scope.data = $scope.data_class0;
    };
          $scope.onSelectTab_class1 = function() {
        console.log("New Tab Selected: ");
        $scope.data = $scope.data_class1;
    };
});