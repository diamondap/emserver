from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def identify(request):
    return Response(request.DATA)
    #return Response({"message": "Hello for today! See you tomorrow!"})
