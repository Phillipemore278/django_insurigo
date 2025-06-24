import os
from django.http import JsonResponse
from django.db import connection
from django.conf import settings

def ping_supabase(request):
    token = request.GET.get("token")

    # Compare token from request with your secret
    expected_token = os.getenv("PING_SECRET", getattr(settings, "PING_SECRET", None))
    if token != expected_token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")  # Lightweight ping to Supabase
        return JsonResponse({"status": "ok", "message": "Supabase pinged"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)