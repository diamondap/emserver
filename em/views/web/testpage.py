from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    """
    Returns a simple test page. This is used for testing parts of the
    application that have to make HTTP requests.
    """
    return render(request, 'testpage.html', {'page_title': 'Test Page'})
