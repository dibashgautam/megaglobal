from django.shortcuts import render, get_object_or_404
from main.models import Category


# 🔹 All Categories Page
def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
        "seo_title": "All Categories | Mega Sewa Global",
        "seo_description": "Browse all machine and product categories available at Mega Sewa Global in Nepal.",
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/category_list.html", context)


# 🔹 Single Category Detail Page
def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    category_description = ""
    if hasattr(category, "description") and category.description:
        category_description = str(category.description).strip()

    if category_description:
        seo_description = category_description[:160]
    else:
        seo_description = f"Explore {category.name} machines and related products from Mega Sewa Global in Nepal."

    context = {
        "category": category,
        "products": products,
        "seo_title": f"{category.name} | Mega Sewa Global",
        "seo_description": seo_description,
        "canonical_url": request.build_absolute_uri(),
    }

    return render(request, "main/category_detail.html", context)