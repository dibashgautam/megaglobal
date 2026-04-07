from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from main.models import Category, Product, Slider


@staff_member_required
def admin_dashboard(request):
    total_categories = Category.objects.count()
    total_products = Product.objects.count()
    total_sliders = Slider.objects.count()
    active_sliders = Slider.objects.filter(is_active=True).count()

    recent_products = Product.objects.select_related("category").order_by("-created_at")[:5]
    recent_categories = Category.objects.order_by("-id")[:5]

    # last 6 months product counts
    today = timezone.now()
    labels = []
    data = []

    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30 * i)
        month_label = month_date.strftime("%b %Y")
        month_products = Product.objects.filter(
            created_at__year=month_date.year,
            created_at__month=month_date.month
        ).count()

        labels.append(month_label)
        data.append(month_products)

    # category wise product count
    category_data = Category.objects.annotate(product_count=Count("products")).values("title", "product_count")

    category_labels = [item["title"] for item in category_data]
    category_counts = [item["product_count"] for item in category_data]

    context = {
        "total_categories": total_categories,
        "total_products": total_products,
        "total_sliders": total_sliders,
        "active_sliders": active_sliders,
        "recent_products": recent_products,
        "recent_categories": recent_categories,
        "monthly_labels": labels,
        "monthly_data": data,
        "category_labels": category_labels,
        "category_counts": category_counts,
    }
    return render(request, "dashboard.html", context)