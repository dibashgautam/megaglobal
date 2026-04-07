from .home import home_view, about, terms
from .category import category_detail_view
from .product import product_detail_view
from .dashboard import admin_dashboard

from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://megasewaglobal.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")