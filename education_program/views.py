from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/admin/',
        '/noticeboard/',
        '/swagger/',
        '/homework/',
        '/qna/',
    ]
    return Response(routes)