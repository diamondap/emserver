from rest_framework.response import Response
from rest_framework.decorators import api_view
from em.libs.routers.identifier import Identifier
from em.libs.registry import get_manager
from em.libs.json_serializable import to_list
from em.models import Router

@api_view(['POST'])
def identify(request):
    body = request.DATA.get('body')
    port = request.DATA.get('port')
    url = request.DATA.get('url')
    headers = request.DATA.get('headers')

    identifier = Identifier(body=body, url=url, port=port, headers=headers)
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
    requests = manager.request_manager.get_login_credentials()
    return Response(to_list(requests))
