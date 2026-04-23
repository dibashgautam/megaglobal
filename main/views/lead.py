import json
import urllib.parse
import urllib.request

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from main.models import Lead


@csrf_exempt   # 👉 development मा ok
@require_POST
def save_lead(request):
    try:
        data = json.loads(request.body)

        phone = data.get("phone", "").strip()
        machine = data.get("machine_requirement", "").strip()
        raw = data.get("raw_material_requirement", "").strip()

        # ✅ atleast 1 required
        if not phone or (not machine and not raw):
            return JsonResponse({
                "success": False,
                "message": "Phone and at least one requirement is required."
            }, status=400)

        lead = Lead.objects.create(
            phone=phone,
            machine_requirement=machine or "",
            raw_material_requirement=raw or ""
        )

        # Google sheet
        nepal_now = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")

        script_url = "https://script.google.com/macros/s/AKfycbxkp0XF5RARb4ioHyUtEmHAk8vSXq2zKlG-RpxABxm5iT11CKe73xVg6ycOUGlAl2O6/exec"

        post_data = urllib.parse.urlencode({
            "lead_id": lead.lead_id,
            "phone": lead.phone,
            "machine_requirement": lead.machine_requirement,
            "raw_material_requirement": lead.raw_material_requirement,
            "created_at": nepal_now,
            "status": "New"
        }).encode("utf-8")

        req = urllib.request.Request(script_url, data=post_data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        urllib.request.urlopen(req, timeout=10)

        request.session["lead_id"] = lead.lead_id

        return JsonResponse({
            "success": True,
            "lead_id": lead.lead_id
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)