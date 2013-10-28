import json
from em import models, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from em import serializers
from em.libs.routers.identifier import Identifier
from em.libs.registry import get_manager



def get_post_data(request):
    return json.loads(request.DATA.get('router_response'))

@api_view(['POST'])
def identify(request):
    post_data = get_post_data(request)
    identifier = Identifier(**post_data)
    router = identifier.identify()
    serializer = serializers.RouterSerializer(router)
    return Response(serializer.data)

@api_view(['GET'])
def get_credentials_requests(request, router_id):
    """
    Returns the requests the client will need to make to
    get router credentials.
    """
    router = models.Router.objects.get(pk=router_id)
    manager = get_manager(router.manufacturer, router.model)
    requests = manager.request_manager.get_login_credentials()
    serializer = serializers.RouterRequestSerializer(requests)
    return Response(serializer.data)

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
    resp = models.RouterResponse(**post_data)

    # Then we find the router manager. We pass in the router's response
    # to get_login_request(). The router manager extracts the login name
    # and password from the router response and tells us what request we
    # need to send to the router to log in. We send that request back to
    # the client.
    router = models.Router.objects.get(pk=router_id)
    manager = get_manager(router.manufacturer, router.model)
    request = manager.request_manager.get_login_request([resp])
    serializer = serializers.RouterRequestSerializer(request)
    return Response(serializer.data)
