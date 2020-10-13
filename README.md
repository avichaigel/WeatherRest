# WeatherRest

This app gets the forecast for the next 7 days for the user, based on his location.
The back-end was written using Django Rest Framework, and the front-end was written using HTML, CSS, JavaScript and jQuery.
The user can choose whichever location he wants on the map, which uses Google Maps API.
The forecast is taken from the OpenWeatherMap API.

PostgreSQL:
There is a seperate file stating how the DB and the table are called.
In the server there is a file called settings.py, in which there is a section called DATABASES. It may need to be changed (for instance the host there is set to "127.0.0.1", so you can change this if you need to).
There is one table called forecast_user, and it has the columns: id, name, password, last_lat, last_lng.
Each user has a row in the table. Each time a user gets a forecast, their row is updated with the location they chose, so next time they log in they get a new forecast for the last location they chose.

Authentication:
Forecasts will only be given to authenticated users, which means users who registered with the password "DWELL123".
Once a user registers or logs in, they can click on a location on the map to ask for a forecast.
Every time the map is clicked, a json including all of users information is sent to the server, who checks that the user has the right password, and if so, returns the forecast. Otherwise, propmts them to register or log in in order to get the forecast.
In order to minimize time while authenticating the user, I created a cache global list, in which I save every user that registers or logs in, and when authenticating the user, I check there first.
