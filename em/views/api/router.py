from rest_framework.decorators import api_view

@api_view(['POST'])
def identify(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
