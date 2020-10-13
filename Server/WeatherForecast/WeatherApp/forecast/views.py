from django.http.response import JsonResponse
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
import datetime

cache = []
password = 'DWELL123'


# authenticate the user who tries to get a forecast, validate the range of the coordinates
# if all is approved, get the forecast from the OpenWeatherMap API
@api_view(['POST'])
def new_forecast(request):
    # parse the accepted json
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    lat, lng = body['last_lat'], body['last_lng']

    # validate the range of the coordinates, and authenticate the user
    if not is_valid_coords(lat, lng):
        return Response('Coordinates are not in the valid range', status.HTTP_404_NOT_FOUND)
    try:
        authenticate(body)
    except ValueError:
        return Response('Please register or log in to see the forecast', status=status.HTTP_401_UNAUTHORIZED)

    # update the user's last_lat and last_lng
    save_user(body)
    return get_forecast(lat, lng)


def save_user(body):
    user_serializer = UserSerializer(data=body)
    if user_serializer.is_valid():
        old_user = User.objects.get(name=body['name'])
        old_user.delete()
        user_serializer.save()

# search the cache for the name of the user who asked for the forecast,
# if he's not there, look for him in the DB. If he's not there either,
# raise a ValueError which will prevent the user from getting the forecast
def authenticate(body):
    # look for the name of the user who asked for the forecast in the cache
    if body['name'] not in cache:
        # if he's not there, look for him in the DB
        try:
            get_user_from_db(body)
        # if he's not in the DB either, raise a ValueError which will prevent the user
        # from getting the forecast
        except ValueError:
            raise ValueError


# get the forecast from OpenWeatherMap API, and create a dictionary
# that will contain the 7 days forecast
def get_forecast(lat, lon):
    # get the forecast from OpenWeatherMap API
    try:
        weather = requests.get('https://api.openweathermap.org/data/2.5/onecall?'
                             'lat='+str(lat)+'&lon='+str(lon)+'&exclude=current,minutely,hourly,alerts&'
                             'appid=8839cc27011b3994d4d5d72ab2e54839&units=imperial&')
    except weather.status_code!=200:
        return JsonResponse({'message': 'Could not retrieve forecast'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # create a dictionary in which the keys are the dates, and the values are a list of:
    # minimal temperature, maximal temperature, and description
    weather_dict = weather.json()
    daily_forecast = {}
    today = True
    for day in weather_dict['daily']:
        if today:
            today = False
            continue
        date_time = str(datetime.datetime.utcfromtimestamp(day['dt']))[:10]
        min_temp = int(day['temp']['min'])
        max_temp = int(day['temp']['max'])
        desc = day['weather'][0]['description']
        daily_forecast[date_time] = [min_temp,max_temp,desc]
    return Response(daily_forecast,status=status.HTTP_200_OK)


# validate the range of the coordinates
def is_valid_coords(lat, lng):
    return -90 <= lat <= 90 and -180 <= lng <= 180


# get the user from the database, if he's not the raise a ValueError
def get_user_from_db(body):
    try:
        user = User.objects.get(name=body['name'], password=body['password'])
        return user
    except User.DoesNotExist:
        raise ValueError


# when a user logs in, authenticate his password,
# and return the last location he asked forecast for
@api_view(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # authenticate user's password
    if body['password'] != password:
        return Response('Wrong password', status.HTTP_401_UNAUTHORIZED)
    # no need to check the cache here because we need to get the user from the db anyways,
    # in order to get the last location he has asked forecast for
    try:
        user = get_user_from_db(body)
    except ValueError:
        return Response('User does not exist, please register first',
                            status=status.HTTP_401_UNAUTHORIZED)
    cache.append(body['name'])
    last_coords = {'last_lat': float(user.last_lat), 'last_lng': float(user.last_lng)}
    return JsonResponse(last_coords, status=status.HTTP_200_OK)


# authenticate user's password, then check if the name is free,
# in the cache and then in the database.
# If all is approved, create new row in our database, which represents a new user
@api_view(['POST'])
def register(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # authenticate user's password, then check if the name is free,
    # in the cache and then in the database.
    if body['password'] != password:
        return Response('Wrong password', status.HTTP_401_UNAUTHORIZED)
    if body['name'] in cache:
        return Response('Username taken', status.HTTP_401_UNAUTHORIZED)
    try:
        user = get_user_from_db(body)
        return Response('Username taken', status.HTTP_401_UNAUTHORIZED)
    except ValueError:
        # body has only username and password, hence set default values for the rest
        body['id'] = 1
        body['last_lat'] = -9999.99
        body['last_lng'] = -9999.99
        # create new row in our database, which represents a new user
        user_serializer = UserSerializer(data=body)
        if user_serializer.is_valid():
            user_serializer.save()
            cache.append(body['name'])
        return Response('Registration completed for ' + body['name'], status.HTTP_200_OK)

