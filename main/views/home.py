# main/views/home.py

from django.shortcuts import render
from django.db.models import Q

from main.models import Category, Product, Slider

from django.db.models import Q

def home_view(request):
    categories = Category.objects.all()
    sliders = Slider.objects.filter(is_active=True)

    query = request.GET.get("q")
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
    }

    return render(request, "main/index.html", context)







def about(request):
    return render(request, 'main/about.html')
def terms(request):
    return render(request, 'main/terms_and_conditions.html')