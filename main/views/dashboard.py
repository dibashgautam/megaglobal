from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count

from main.models import Product, Category, Visitor


@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_visitors = Visitor.objects.count()
    guest_visitors = Visitor.objects.filter(is_guest=True).count()

    categories = Category.objects.annotate(product_count=Count("products"))

    category_data = []
    category_labels = []
    category_counts = []

    for category in categories:
        count = category.product_count
        percent = round((count / total_products) * 100, 2) if total_products else 0

        category_data.append({
            "name": category.title,
            "count": count,
            "percent": percent,
        })

        category_labels.append(category.title)
        category_counts.append(count)

    top_viewed_machines = Product.objects.order_by("-view_count")[:10]

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_visitors": total_visitors,
        "guest_visitors": guest_visitors,
        "category_data": category_data,
        "category_labels": category_labels,
        "category_counts": category_counts,
        "top_viewed_machines": top_viewed_machines,
    }

    return render(request, "admin/custom_dashboard.html", context)