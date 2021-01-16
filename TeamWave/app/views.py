from datetime import datetime, timezone
import json
import requests

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from . import models


class Search(APIView):
    renderer_classes = [JSONRenderer]   
    def post(self, request):
        '''
            Handling POST request on the particular url.

        Args:
            request obj: Request Object.

        Returns;
            Response obj: Returns Django Response opbject.
        '''
        valid, error = self.validate(self.request.data)
        if not valid:
            return Response({
                "message": error
            }, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_search_limit_available(self.request.data['email']):
            return Response({
                "message": "Search Limit Exceeded"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Checking is the search query is already searched or not.
        if self.request.data['query'] in cache:
            return Response(cache.get(self.request.data['query']))

        result = self.search(self.request.data['query'], self.request.data['params'])

        # Storing result in the cache.
        cache.set(self.request.data['query'], result)
        return Response(cache.get(self.request.data['query']))


    def validate(self, data):
        '''
            Validate incoming request json data.

        Args:
            data dict: Incoming Json data.

        Returns:
            tuple: Return tuple contaning status of incoming data and error.
        '''
        valid_keys = ['email', 'query', 'params']

        for key in valid_keys:
            if not key in data:
                return (False, {"include " + key + " in the data"})

        return (True, {})


    def search(self, query, params):
        '''
            Request StackOverFlow api for searching questions.

        Args:
            query str: The query for which the question to be searched.
            params list: List contaning all available fields/parameters.

        Returns:
            json: Returns json of the desired result.
        '''
        base_url = (
            'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&site=stackoverflow')

        base_url = base_url + ('&' + query)
        for arg in params:
            base_url = base_url + ('&' + arg)

        response = requests.get(base_url)
        return json.loads(response.content.decode('utf-8'))


    def is_search_limit_available(self, email):
        '''
            Check search limit of a particular session.

        Args:
            email str: Email of the particular user for processing its session.

        Returns:
            bool: Return True/False on the successfully validating session.
        '''

        query_set = models.User.objects.filter(email=email)
        if len(query_set) == 0:
            usr_obj = models.User(email=email, last_time_search=datetime.now(timezone.utc), num_of_query=1)
            usr_obj.save()
            return True

        usr_obj = query_set[0]
        delta_time = datetime.now(timezone.utc) - usr_obj.last_time_search

        if (delta_time.seconds <=60 and usr_obj.num_of_query >=5) or (
            delta_time.days == 0 and usr_obj.num_of_query >=100):
            return False

        # Starting New Today's Session.
        if delta_time.days > 0:
            usr_obj.last_time_search = datetime.now()
            usr_obj.num_of_query = 0

        usr_obj.num_of_query = usr_obj.num_of_query + 1
        usr_obj.save()
        return True
