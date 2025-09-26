from django.http import HttpResponse, JsonResponse

def home_html_view(request):
    return HttpResponse("This is home_html_view")

def home_view(request):
    return JsonResponse({"message": "This is home_view"})

def api_providers(request):
    return JsonResponse({"providers": []})

def api_bundles(request):
    return JsonResponse({"bundles": []})

def api_bundles_by_provider(request, provider_id):
    return JsonResponse({"provider_id": provider_id, "bundles": []})

def api_routers(request):
    return JsonResponse({"routers": []})

def api_create_order(request):
    return JsonResponse({"order_created": True})
