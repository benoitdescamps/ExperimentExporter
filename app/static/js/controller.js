

var myApp = angular.module('myApp',['infinite-scroll']);
myApp.controller('DataController', function($rootScope,$scope,$http) {
 $scope.selected_experiment_property = 0;
   $http.get("/s/").then(function(r) {
                    $scope.data = r.data.all_experiments.new_project;

                     console.log($scope.data)
                     $scope.plot_data = $scope.data;
    $scope.selected_property = 'model_properties';
    $scope.selected_experiment =  $scope.data[0];
    $scope.selected_experiment_property = $scope.selected_experiment[$scope.selected_property];

    var name_container_plot = 'div.container_experiment_plot';

   // data that you want to plot, I've used separate arrays for x and y values

   //project should remember start project
   // timestamp is for axis label
   // replace timestamp by day since
    var data = $scope.plot_data;
    var N_experiments = data.length;
    xdata = Array.apply(null, {length: N_experiments}).map(Number.call, Number)//[5, 10, 15, 20],
    ydata = Array.apply(null, {length: N_experiments}).map(Number.call, Number);// [3, 17, 4, 6];
         // size and margins for the chart
        var margin = {
          top: 20,
          right: 15,
          bottom: 60,
          left: 60
        }, width = 300 - margin.left - margin.right,
          height = 300 - margin.top - margin.bottom;
        var x = d3.scale.linear()
          .domain([0, 10])
          .range([0, width]);
        var y = d3.scale.linear()
          .domain([0, 10])
          .range([height, 0]);
        var chart = d3.select(name_container_plot)
          .append('svg')
          .attr('width', width + margin.right + margin.left)
          .attr('height', height + margin.top + margin.bottom)
          .attr('class', 'chart')
         var main = chart.append('g')
          .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
          .attr('width', width)
          .attr('height', height)
          .attr('class', 'main')
         // draw the x axis
         var xAxis = d3.svg.axis()
          .scale(x)
          .orient('bottom');
        main.append('g')
          .attr('transform', 'translate(0,' + height + ')')
          .attr('class', 'main axis date')
          .call(xAxis);
         // draw the y axis
        var yAxis = d3.svg.axis()
          .scale(y)
          .orient('left');
        main.append('g')
          .attr('transform', 'translate(0,0)')
          .attr('class', 'main axis date')
          .call(yAxis);
         // draw the graph object
        var g = main.append("svg:g");
        g.selectAll("scatter-dots")
          .data(data)
          .enter().append("svg:circle")
          .attr("cy", function(d) {
            return y(d.metrics.r2_score*10);
          })
          .attr("cx", function(d, i) {
            return x(d.days_since_start);
          })
          .attr("r", 10)
          .style("opacity", 0.6)
          .on('mouseover',handleMouseOver)




    $scope.onMouseOver = function(experiment){
        console.log("mouse over user: " + experiment.timestamp)
        $scope.selected_experiment =  experiment;
        console.log($scope.selected_experiment_property);
        $scope.selected_experiment_property = $scope.selected_experiment[$scope.selected_property];
        console.log($scope.selected_experiment_property);
    };
    function handleMouseOver(d, i) {
            setExperimentProperty(d,$scope.selected_property);
          };


function getExperimentProperty(){
    var div_tabel = document.getElementsByClassName('container_experiment_properties')[0];
    return div_tabel.getAttribute("data-value");
}
function setExperimentProperty(experiment,property){
    var div_tabel = document.getElementsByClassName('container_experiment_properties')[0];
    div_tabel.setAttribute("data-value",experiment[property] );
    $scope.selected_experiment_property = experiment[property];
    console.log( $scope.selected_experiment_property );
}


//

});

});