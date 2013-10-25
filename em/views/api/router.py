from rest_framework.response import Response
from rest_framework.decorators import api_view
from em.libs.routers.identifier import Identifier
from em.libs.registry import get_manager
from em.libs.json_serializable import list_to_json, list_from_json
from em.models import Router

@api_view(['POST'])
def identify(request):
    html = request.DATA.get('html')
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

@api_view(['GET'])
def get_credentials_requests(request, router_id):
    """
    Returns the requests the client will need to make to
    get router credentials.
    """
    router = Router.objects.get(pk=router_id)
    manager = get_manager(router.manufacturer, router.model)
    # TODO: Fix get_manager so it returns only one object!
    requests = manager[0].request_manager.get_login_credentials()
    return Response(list_to_json(requests))
