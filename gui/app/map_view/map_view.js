'use strict';

angular.module('myApp.map_view', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/map_view', {
            templateUrl: 'map_view/map_view.html',
            controller: 'MapViewCtrl'
        });
    }])

    .controller("MapViewCtrl", function ($scope, $http) {
        // URL
        var places_api_url = 'http://localhost:8080/places';
        var weather_api_url = 'http://localhost:8080/weather';
        var uber_api_url = 'http://localhost:8080/uber';
        var instagram_api_url = 'http://localhost:8080/instagram';
        var sky_scanner_api_url = 'http://localhost:8080/skyscanner';

        // MESSAGE
        var select_cities = "Please select cities first. Cities must be different for source and destination!";
        var loading_data = "Loading data...";
        var no_data = "No data found! Maybe there's no particular service in this city?";
        var error_on_retrieving_data = "Error while retrieving data!";

        // BOOTSTRAP PANEL / ALERT CLASSES
        var alert_class_hidden = "ng-hide";
        var alert_class_loading = "alert-info";
        var alert_class_failure = "alert-danger";
        var alert_class_warning = "alert-warning";
        var alert_message = "";

        $scope.places = [];
        $scope.source_city = null;
        $scope.destination_city = null;

        $scope.weather_forecast_alert_class = alert_class_hidden;
        $scope.weather_forecast_alert_message = alert_message;
        $scope.weather_forecast = [];

        $scope.uber_pricing_alert_class = alert_class_hidden;
        $scope.uber_pricing_alert_message = alert_message;
        $scope.uber_pricing = [];

        $scope.instagram_media_alert_class = alert_class_hidden;
        $scope.instagram_media_alert_message = alert_message;
        $scope.instagram_media = [];

        $scope.sky_scanner_flights_alert_class = alert_class_hidden;
        $scope.sky_scanner_flights_alert_message = alert_message;
        $scope.sky_scanner_flights = [];

        $http.get(places_api_url)
            .success(function (data) {
                $scope.places = eval(data);
            })
            .error(function (data) {
                console.error('Error on retrieving Places: ' + data);
            });

        $scope.setSourceCity = function (city) {
            console.log('Setting source city: ' + city.city_name);
            $scope.source_city = city;
        };

        $scope.setDestinationCity = function (city) {
            console.log('Setting destination city: ' + city.city_name);
            $scope.destination_city = city;
        };

        $scope.loadBackendData = function () {
            if ($scope.source_city !== null
                && $scope.destination_city !== null
                && $scope.source_city.city_name !== $scope.destination_city.city_name) {
                var dest_city_json = angular.toJson($scope.destination_city);

                $scope.weather_forecast = [];
                $scope.weather_forecast_alert_class = alert_class_loading;
                $scope.weather_forecast_alert_message = loading_data;
                $http.post(weather_api_url, dest_city_json).success(function (data, status, headers, config) {
                    if (data.length > 0) {
                        $scope.weather_forecast_alert_class = alert_class_hidden;
                        $scope.weather_forecast_alert_message = alert_message;
                        $scope.weather_forecast = data;
                    }
                    else {
                        $scope.weather_forecast_alert_class = alert_class_warning;
                        $scope.weather_forecast_alert_message = no_data;
                    }

                }).error(function (data, status, headers, config) {
                    $scope.weather_forecast_alert_class = alert_class_failure;
                    $scope.weather_forecast_alert_message = error_on_retrieving_data;
                    console.log('Did not retrieve Weather data! ' + status + ' ' + data);
                });

                $scope.uber_pricing = [];
                $scope.uber_pricing_alert_class = alert_class_loading;
                $scope.uber_pricing_alert_message = loading_data;
                $http.post(uber_api_url, dest_city_json).success(function (data, status, headers, config) {
                    if (data.length > 0) {
                        $scope.uber_pricing_alert_class = alert_class_hidden;
                        $scope.uber_pricing_alert_message = alert_message;
                        $scope.uber_pricing = data;
                    }
                    else {
                        $scope.uber_pricing_alert_class = alert_class_warning;
                        $scope.uber_pricing_alert_message = no_data;
                    }
                }).error(function (data, status, headers, config) {
                    $scope.uber_pricing_alert_class = alert_class_failure;
                    $scope.uber_pricing_alert_message = error_on_retrieving_data;
                    console.error('Did not retrieve Uber data! ' + status + ' ' + data);
                });

                $scope.instagram_media = [];
                $scope.instagram_media_alert_class = alert_class_loading;
                $scope.instagram_media_alert_message = loading_data;
                $http.post(instagram_api_url, dest_city_json).success(function (data, status, headers, config) {
                    if (data.length > 0) {
                        $scope.instagram_media_alert_class = alert_class_hidden;
                        $scope.instagram_media_alert_message = alert_message;
                        $scope.instagram_media = data;
                    }
                    else {
                        $scope.instagram_media_alert_class = alert_class_warning;
                        $scope.instagram_media_alert_message = no_data;
                    }
                }).error(function (data, status, headers, config) {
                    $scope.instagram_media_alert_class = alert_class_failure;
                    $scope.instagram_media_alert_message = error_on_retrieving_data;
                    console.error('Did not retrieve Instagram data! ' + status + ' ' + data);
                });

                $scope.sky_scanner_flights = [];
                $scope.sky_scanner_flights_alert_class = alert_class_loading;
                $scope.sky_scanner_flights_alert_message = loading_data;
                var request = angular.toJson({"city_a": $scope.source_city, "city_b": $scope.destination_city});
                console.log("Retrieving SkyScanner for: " + request);
                $http.post(sky_scanner_api_url, request).success(function (data, status, headers, config) {
                    if (data.length > 0) {
                        $scope.sky_scanner_flights_alert_class = alert_class_hidden;
                        $scope.sky_scanner_flights_alert_message = alert_message;
                        $scope.sky_scanner_flights = data;
                    }
                    else {
                        $scope.sky_scanner_flights_alert_class = alert_class_warning;
                        $scope.sky_scanner_flights_alert_message = no_data;
                    }
                }).error(function (data, status, headers, config) {
                    $scope.sky_scanner_flights_alert_class = alert_class_failure;
                    $scope.sky_scanner_flights_alert_message = error_on_retrieving_data;
                    console.error('Did not retrieve SkyScanner data! ' + status + ' ' + data);
                });
            }
            else {
                $scope.weather_forecast_alert_class = alert_class_warning;
                $scope.weather_forecast_alert_message = select_cities;

                $scope.uber_pricing_alert_class = alert_class_warning;
                $scope.uber_pricing_alert_message = select_cities;

                $scope.instagram_media_alert_class = alert_class_warning;
                $scope.instagram_media_alert_message = select_cities;

                $scope.sky_scanner_flights_alert_class = alert_class_warning;
                $scope.sky_scanner_flights_alert_message = select_cities;
            }

        };
    })
    .directive('mapDir', function () {
        // return {
        //     restrict: 'A',
        //     link: function ($scope) {
        //         var map = new ol.Map({
        //             target: 'map',
        //             layers: [
        //                 new ol.layer.Tile({
        //                     source: new ol.source.OSM()
        //                 })
        //             ],
        //             view: new ol.View({
        //                 center: ol.proj.fromLonLat([13.40, 52.52]),
        //                 zoom: 4
        //             })
        //         });
        //     }
        // };
    });