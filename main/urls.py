from django.urls import path, reverse
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap

from main.views import home_view, about, terms, robots_txt, admin_dashboard
from main.views.product import product_list_view, product_detail_view, live_search_view
from main.views.category import category_list_view, category_detail_view
from main.models import Product, Category
from main.views.lead import save_lead


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all().order_by("-updated_at")

    def location(self, obj):
        return reverse("product_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all().order_by("-updated_at")

    def location(self, obj):
        return reverse("category_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "terms", "product_list", "category_list"]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "static": StaticSitemap,
    "products": ProductSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    path("save-lead/", save_lead, name="save_lead"),
    path("", home_view, name="home"),
    path("about/", about, name="about"),
    path("terms/", terms, name="terms"),

    path("categories/", category_list_view, name="category_list"),
    path("categories/<slug:slug>/", category_detail_view, name="category_detail"),

    path("products/", product_list_view, name="product_list"),
    path("products/<slug:slug>/", product_detail_view, name="product_detail"),

    path("live-search/", live_search_view, name="live_search"),

    # path("dashboard/", admin_dashboard, name="dashboard"),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]