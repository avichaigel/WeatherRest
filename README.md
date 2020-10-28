# WeatherRest

This app gets the forecast for the next 7 days for the user, based on his location.
The back-end was written using Django Rest Framework, and the front-end was written using HTML, CSS, JavaScript and jQuery.
The user can choose whichever location he wants on the map, which uses Google Maps API.
The forecast is taken from the OpenWeatherMap API.

***Important:*** For the purpose of authentication, the only acceptable password is DWELL123. This is detailed below. 

### Running:
1. To run the server, open it in an IDE (I used PyCharm) and in the terminal run the commands:
cd WeatherApp (should lead you into .../WeatherForecast/WeatherApp)
python manage.py runserver 8080

2. To run the client, open it in an IDE (I used Visual Studio) and run it from there (F5).

3. When I run my client it runs on localhost:10202. If yours uses another port, or not on localhost, you will need to add your client's address to the server, by adding it to the CORS_ORIGIN_WHITELIST part in the file "settings.py" which is inside .../WeatherForecast/WeatherApp.
Most chances are you will not need to change this.

### PostgreSQL:
There is a seperate file stating how the DB and the table are called.
In the server there is a file called settings.py, in which there is a section called DATABASES. It may need to be changed (for instance the host there is set to "127.0.0.1", so you can change this if you need to).
There is one table called forecast_user, and it has the columns: id, name, password, last_lat, last_lng.
Each user has a row in the table. Each time a user gets a forecast, their row is updated with the location they chose, so next time they log in they get a new forecast for the last location they chose.

### Authentication:
Forecasts will only be given to authenticated users, which means users who registered with the password "DWELL123".
Once a user registers or logs in, they can click on a location on the map to ask for a forecast.
Every time the map is clicked, a json including all of users information is sent to the server, who checks that the user has the right password, and if so, returns the forecast. Otherwise, propmts them to register or log in in order to get the forecast.
In order to minimize time while authenticating the user, I created a cache global list, in which I save every user that registers or logs in, and when authenticating the user, I check there first.

### Production:
In order to get the project ready for production, debug mode should me changed to False in settings.py, the database should be on a cloud, and the Google Maps key should be restricted.
After consulting with someone from the industry, I understood that it's better to hand in such a project with a local database, but in order to change the database to be on the cloud, simply go to settings.py and remove the commenting out that I did to the settings of the cloud database I have on ElephantSQL, and comment out the settings of the local databse.
Regarding the debug mode and key restriction - I did that and it caused some problems which could probably be solved easily, but deadline is near and I don't feel so well, so eventually I left debug mode on, and did not restrict the key.
