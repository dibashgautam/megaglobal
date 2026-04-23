from django.contrib.admin import AdminSite
from django.db.models import Count

from .models import Product, Category, Visitor


class MegaSewaAdminSite(AdminSite):
    site_header = "Mega Sewa Global Admin Panel"
    site_title = "Mega Sewa Global Admin"
    index_title = "Welcome to Mega Sewa Global Dashboard"
    index_template = "admin/index.html"
    login_template = "admin/login.html"

    def index(self, request, extra_context=None):
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

        top_viewed_machines = Product.objects.select_related("category").order_by("-view_count")[:10]

        extra_context = extra_context or {}
        extra_context.update({
            "total_products": total_products,
            "total_categories": total_categories,
            "total_visitors": total_visitors,
            "guest_visitors": guest_visitors,
            "category_data": category_data,
            "category_labels": category_labels,
            "category_counts": category_counts,
            "top_viewed_machines": top_viewed_machines,
        })

        return super().index(request, extra_context=extra_context)


admin_site = MegaSewaAdminSite(name="mega_admin")