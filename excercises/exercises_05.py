import requests

from django.http import JsonResponse
from django.views import View


# Create an API view that returns a basic JSON response

class ThisApiView(View):
    def get(self, request):
        api_url = 'https://api.example.com'
        headers = {'Content-Type': 'application/json'}
        resp = {
            'variable_1': 'value_1',
            'variable_2': 'value_2',
        }
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            resp = response.json()
        except requests.exceptions.RequestException as e:
            print(e)
        return JsonResponse(resp)
