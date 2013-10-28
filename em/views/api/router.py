import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from em.libs.routers.identifier import Identifier
from em.libs.registry import get_manager
from em.libs.json_serializable import to_list
from em.models import Router
from em.libs.http import RouterRequest, RouterResponse

def get_post_data(request):
    body = request.DATA.get('body')
    url = request.DATA.get('url')
    headers = request.DATA.get('headers')
    return {'body': body, 'url': url, 'headers': headers}

@api_view(['POST'])
def identify(request):
    post_data = get_post_data(request)
    post_data['port'] = request.DATA.get('port')
    identifier = Identifier(**post_data)
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

@api_view(['POST'])
def get_login_request(request, router_id):
    """
    Returns the requests the client will need to make to
    get router credentials.
    """
    # The remote client has already sent a request to the router and
    # gotten a response. It forwards that response in the POST. We
    # construct a RouterResponse from it...
    post_data = get_post_data(request)
    post_data['method'] = request.DATA.get('method')
    post_data['status_code'] = request.DATA.get('status_code')
    resp = RouterResponse(**post_data)

    # Then we find the router manager. We pass in the router's response
    # to get_login_request(). The router manager extracts the login name
    # and password from the router response and tells us what request we
    # need to send to the router to log in. We send that request back to
    # the client.
    router = Router.objects.get(pk=router_id)
    manager = get_manager(router.manufacturer, router.model)
    request = manager.request_manager.get_login_request([resp])
    return Response(request)
