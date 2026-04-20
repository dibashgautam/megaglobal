from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from main.models import Category, Product, Slider


def home_view(request):
    categories = Category.objects.all()
    sliders = Slider.objects.filter(is_active=True).order_by("order")

    query = request.GET.get("q", "").strip()
    products = Product.objects.select_related("category").all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = products[:8]

    context = {
        "categories": categories,
        "products": products,
        "sliders": sliders,
        "query": query,
        "seo_title": "Mega Sewa Global | Machine Seller in Nepal",
        "seo_description": "Buy industrial machines and equipment in Nepal from Mega Sewa Global. Browse categories, products, and contact directly on WhatsApp.",
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/index.html", context)


def about(request):
    context = {
        "seo_title": "About Us | Mega Sewa Global",
        "seo_description": "Learn more about Mega Sewa Global and our machine supply services in Nepal.",
        "canonical_url": request.build_absolute_uri(),
    }
    return render(request, "main/about.html", context)


def terms(request):
    context = {
        "seo_title": "Terms and Conditions | Mega Sewa Global",
        "seo_description": "Read the terms and conditions of Mega Sewa Global.",
        "canonical_url": request.build_absolute_uri(),
    }
    return render(request, "main/terms_and_conditions.html", context)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Sitemap: https://megasewaglobal.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")