var server = "http://localhost:8080";

$(document).ready(
    {

    });

// Google Maps API for JavaScript. Clicking the map gets a forecast if user is authenticated
function initMap() {
    var myLatlng = { lat: -25.363, lng: 131.044 };

    var map = new google.maps.Map(
        document.getElementById("map"), { zoom: 3, center: myLatlng });

    // Create the initial InfoWindow.
    var infoWindow = new google.maps.InfoWindow(
        { content: "Click the map to get the forecast for any location!", position: myLatlng });
    infoWindow.open(map);

    // Configure the click listener.
    map.addListener("click", function (mapsMouseEvent) {
        var coords = {
            last_lat: mapsMouseEvent.latLng.lat(),
            last_lng: mapsMouseEvent.latLng.lng()
        };
        //get the forecast
        getForecastByCoords(coords);

        // Close the current InfoWindow.
        infoWindow.close();

        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({ position: mapsMouseEvent.latLng });
        infoWindow.setContent(mapsMouseEvent.latLng.toString());
        infoWindow.open(map);
    });
}

//
function getForecastByCoords(coords) {

    //authentication - every time a user asks for a forecast, we send their details to the server,
    //there we check if these details meet the requirements, and if so - forecast is shown
    var details = {id: 1,
        name: $("#loginUserName").val(),
        password: $("#LoginPass").val(),
        last_lat: coords.last_lat,
        last_lng: coords.last_lng
    }

    //an asynchronous POST request is sent to the server,
    //to fetch the forecast for the clicked location 
    var res = $.ajax({
        method: "POST",
        url: server + "/api/forecast",
        async: true,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(details),
        dataType: "json",
        success: function (data) {

            //create a table with the forecast
            $("#tbl tbody").empty();
            var $tbl = $("#tbl");
            $.each(data,
                function (key, value) {

                    var date = key;
                    var minTemp = value[0];
                    var maxTemp = value[1];
                    var desc = value[2];

                    if (!date)
                        return;

                    var $tr = $("<tr>").append(
                        $("<td>").text(date),
                        $("<td>").text(minTemp),
                        $("<td>").text(maxTemp),
                        $("<td>").text(desc)
                    );
                    $tbl[0].innerHTML += $tr.html();
                    console.log($tr.wrap("<p>").html());
                });
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }
    });

    return res == "True";

}

//
function login() {

    var login = {
        name: $("#loginUserName").val(),
        password: $("#LoginPass").val()
    }

    var res = $.ajax({
        method: "POST",
        url: server + "/api/login",
        async: true,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(login),
        dataType: "json",
        success: function (coords) {
            if (coords.last_lat < -998 && coords.last_lng < -998) {
                alert("Welcome " + login.name +"!\n" +
                    "No previous location has been chosen yet,\n" +
                    "would you like to give it a try?")
                return;
            } else {
                alert("Welcome " + login.name + "!\n" +
                    "Showing forecast for the last location you have chosen:\n" +
                    coords.last_lat + ", " + coords.last_lng);
            }
            getForecastByCoords(coords);
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
            return;
        }
    });
    return res == "True";

}

function register() {
    var newUser = {
        name: $("#RegUserName").val(),
        password: $("#RegPass").val()
    }

    var res = $.ajax({
        method: "POST",
        url: server + "/api/register",
        async: true,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newUser),
        dataType: "json",
        success: function () {
            alert("Registration successful, you are now logged in as " + newUser.name);
            $("#loginUserName").val($("#RegUserName").val());
            $("#LoginPass").val($("#RegPass").val());
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }
    });
    return res == "True";

}

function password_visibility(id) {
    var x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}