import os
import logging
from django.http import JsonResponse
from django.db import connection, connections
from django.conf import settings

logger = logging.getLogger(__name__)

def ping_supabase(request):
    token = request.GET.get("token")

    expected_token = os.getenv("PING_SECRET", getattr(settings, "PING_SECRET", None))
    if token != expected_token:
        logger.warning("Unauthorized ping attempt")
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        connections.close_all()  # close stale connections

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        logger.info("Supabase ping successful")
        return JsonResponse({"status": "ok", "message": "Supabase pinged"})
    except Exception as e:
        logger.error(f"Supabase ping failed: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

