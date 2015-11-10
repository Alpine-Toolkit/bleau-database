var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
var map;

function initialize() {
  var myOptions = {
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  }

  map = new google.maps.Map(document.getElementById("map"), myOptions);
  directionsDisplay.setMap(map);
  directionsDisplay.setPanel(document.getElementById("directions_panel"));
  compute_route();
}

function compute_route() {
  var way_points = [];
  switch(destination_name) {
  case "Carrefour du Bas Bréau" :
    way_points[0] = {location:"48.4548797, 2.6047897", stopover:true};
    way_points[1] = {location:"48.4458280, 2.6122141", stopover:true};
    way_points[2] = {location:"48.4453013, 2.6117635", stopover:true};
    break;
  case "Parking de la Croix Saint Jérome" :
    way_points[0] = {location:"48.39226, 2.50647", stopover:true};
    break;
  case "Eléphant" :
    way_points[0] = {location:"48.317285, 2.570815", stopover:true};
    break;
  case "Rocher de Milly":
  case "Bois Rond" :
  case "Parking de la Canche aux Merciers" :
    way_points[0] = {location:"Macherin", stopover:true};
    break;
  case "J.A. Martin" :
    way_points[0] = {location:"48.456232, 2.518678", stopover:true};
  }

  var request = {
    // entrée A6A porte d'Orléans
    origin: "48.8196301, 2.3268270",
    destination: destination,
    waypoints: way_points,
    optimizeWaypoints: true,
    travelMode: google.maps.DirectionsTravelMode.DRIVING
  }

  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
      compute_total_distance(directionsDisplay.directions);
    }
  });
}

function compute_total_distance(result) {
  var sum = 0;
  var route = result.routes[0];
  for (i = 0; i < route.legs.length; i++) {
    sum += route.legs[i].distance.value;
  }
  var total = Math.round(sum / 1000.);
  document.getElementById("total").innerHTML = total + " km";
}
