from rest_framework.response import Response
from rest_framework.decorators import api_view
from em.libs.routers.identifier import Identifier
from em.models import Router

@api_view(['POST'])
def identify(request):
    html = request.DATA.get('body')
    port = request.DATA.get('port')
    url = request.DATA.get('url')
    headers = request.DATA.get('headers')

    identifier = Identifier(html=html, url=url, port=port, headers=headers)
    router = identifier.identify()
    return Response({"manufacturer": router.manufacturer,
                     "model": router.model,
                     "firmware_version": router.firmware_version,
                     "auth_protocol": router.auth_protocol,
                     "id": router.id})
    #return Response(request.DATA)
    #return Response({"message": "Hello for today! See you tomorrow!"})
