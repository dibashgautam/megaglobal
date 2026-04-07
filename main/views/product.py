from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from main.models import Product


# 🔹 All Products Page
def product_list_view(request):
    products = Product.objects.select_related("category").all()

    context = {
        "products": products,
        "seo_title": "All Machines | Mega Sewa Global",
        "seo_description": "Explore all industrial machines and products available at Mega Sewa Global in Nepal.",
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/product_list.html", context)


# 🔹 Single Product Detail Page
def product_detail_view(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)

    # SEO Title
    seo_title = f"{product.title} in Nepal | Mega Sewa Global"

    # SEO Description
    product_description = ""
    if hasattr(product, "description") and product.description:
        product_description = str(product.description).strip()

    if product_description:
        seo_description = product_description[:160]
    else:
        seo_description = f"Buy {product.title} in Nepal from Mega Sewa Global. High quality machine, trusted support and competitive pricing."

    context = {
        "product": product,
        "seo_title": seo_title,
        "seo_description": seo_description,
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/product_detail.html", context)


# 🔹 Live Search
def live_search_view(request):
    query = request.GET.get("q", "").strip()

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query)
        )[:5]

        data = [
            {
                "title": product.title,
                "slug": product.slug,
                "price": str(product.final_price),
                "image": product.image.url if product.image else "",
            }
            for product in products
        ]
    else:
        data = []

    return JsonResponse(data, safe=False)