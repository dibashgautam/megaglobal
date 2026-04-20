from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils.html import strip_tags

from main.models import Product, Visitor


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def product_list_view(request):
    products = Product.objects.select_related("category").all()

    context = {
        "products": products,
        "seo_title": "All Machines | Mega Sewa Global",
        "seo_description": "Explore all industrial machines and products available at Mega Sewa Global in Nepal.",
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/product_list.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("gallery"),
        slug=slug
    )

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    already_counted = Visitor.objects.filter(
        session_key=session_key,
        product=product
    ).exists()

    if not already_counted:
        product.view_count += 1
        product.save(update_fields=["view_count"])

        Visitor.objects.create(
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None,
            product=product,
            is_guest=not request.user.is_authenticated,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")
        )

    clean_description = strip_tags(product.description).strip() if product.description else ""

    seo_title = product.meta_title if product.meta_title else f"Buy {product.title} in Nepal | Mega Sewa Global"

    if product.meta_description:
        seo_description = product.meta_description[:160]
    elif clean_description:
        seo_description = clean_description[:160]
    else:
        seo_description = f"Buy {product.title} in Nepal from Mega Sewa Global. High quality machine, trusted support and competitive pricing."

    related_products = Product.objects.select_related("category").filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products,
        "seo_title": seo_title,
        "seo_description": seo_description,
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/product_detail.html", context)


def live_search_view(request):
    query = request.GET.get("q", "").strip()

    if len(query) >= 2:
        products = Product.objects.select_related("category").filter(
            Q(title__icontains=query)
        )[:5]

        data = [
            {
                "title": product.title,
                "slug": product.slug,
                "url": product.get_absolute_url(),
                "price": str(product.final_price),
                "image": product.image.url if product.image else "",
                "category": product.category.title if product.category else "",
            }
            for product in products
        ]
    else:
        data = []

    return JsonResponse(data, safe=False)