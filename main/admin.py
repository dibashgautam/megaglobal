from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Slider
from .admin_site import admin_site


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "title", "slug", "updated_at")
    search_fields = ("title",)
    readonly_fields = ("slug", "image_preview")

    fields = (
        "title",
        "slug",
        "image",
        "image_preview",
        "description",
    )

    class Media:
        js = ("js/admin_image_preview.js",)

    def image_preview(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<div class="admin-main-preview-box">'
                '<img src="{}" id="category-image-preview" alt="Category Preview" '
                'style="display:block;max-width:260px;max-height:260px;object-fit:cover;'
                'border-radius:12px;border:1px solid #ddd;">'
                '</div>',
                obj.image.url
            )

        return format_html(
            '<div class="admin-main-preview-box">'
            '<img src="{}" id="category-image-preview" alt="Category Preview" '
            'style="display:none;max-width:260px;max-height:260px;object-fit:cover;'
            'border-radius:12px;border:1px solid #ddd;">'
            '<span id="category-image-placeholder" class="preview-placeholder">{}</span>'
            '</div>',
            "",
            "No Image Preview"
        )

    image_preview.short_description = "Preview"

    def image_tag(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;'
                'border-radius:10px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = "Image"


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    min_num = 0
    fields = ("image", "image_preview")
    readonly_fields = ("image_preview",)
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"

    class Media:
        js = ("js/admin_image_preview.js",)

    def image_preview(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<div class="admin-inline-preview-box">'
                '<img src="{}" class="admin-live-preview inline-image-preview" '
                'alt="Preview" style="max-width:220px;max-height:220px;'
                'object-fit:cover;border-radius:12px;border:1px solid #ddd;">'
                '</div>',
                obj.image.url
            )
        return format_html(
            '<div class="admin-inline-preview-box">'
            '<img src="{}" class="admin-live-preview inline-image-preview" alt="Preview" '
            'style="display:none;max-width:220px;max-height:220px;object-fit:cover;'
            'border-radius:12px;border:1px solid #ddd;">'
            '<span class="preview-placeholder">{}</span>'
            '</div>',
            "",
            "No Preview"
        )

    image_preview.short_description = "Preview"


@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "title",
        "category",
        "view_count",
        "original_price",
        "discount_percent",
        "final_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("title", "meta_title", "meta_description")
    list_select_related = ("category",)
    readonly_fields = ("slug", "main_image_preview", "final_price", "created_at", "updated_at")

    fields = (
        "title",
        "slug",
        "category",
        "image",
        "main_image_preview",
        "original_price",
        "discount_percent",
        "final_price",
        "description",
        "meta_title",
        "meta_description",
        "created_at",
        "updated_at",
    )

    inlines = [ProductImageInline]

    class Media:
        js = ("js/admin_image_preview.js",)

    def main_image_preview(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<div class="admin-main-preview-box">'
                '<img src="{}" id="main-image-preview" alt="Main Preview" '
                'style="max-width:260px;max-height:260px;object-fit:cover;'
                'border-radius:12px;border:1px solid #ddd;">'
                '</div>',
                obj.image.url
            )
        return format_html(
            '<div class="admin-main-preview-box">'
            '<img src="{}" id="main-image-preview" alt="Main Preview" '
            'style="display:none;max-width:260px;max-height:260px;object-fit:cover;'
            'border-radius:12px;border:1px solid #ddd;">'
            '<span id="main-image-placeholder" class="preview-placeholder">{}</span>'
            '</div>',
            "",
            "No Image Preview"
        )

    main_image_preview.short_description = "Main Image Preview"

    def image_tag(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<img src="{}" style="width:55px;height:55px;object-fit:cover;'
                'border-radius:10px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = "Image"


@admin.register(Slider, site=admin_site)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("slider_image_preview", "title", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")
    readonly_fields = ("slider_image_preview", "created_at")

    fields = (
        "title",
        "subtitle",
        "image",
        "slider_image_preview",
        "order",
        "is_active",
        "created_at",
    )

    class Media:
        js = ("js/admin_image_preview.js",)

    def slider_image_preview(self, obj):
        if obj and obj.image and hasattr(obj.image, "url"):
            return format_html(
                '<div class="admin-slider-preview-box">'
                '<img src="{}" id="slider-image-preview" alt="Slider Preview" '
                'style="max-width:260px;max-height:180px;object-fit:cover;'
                'border-radius:12px;border:1px solid #ddd;">'
                '</div>',
                obj.image.url
            )
        return format_html(
            '<div class="admin-slider-preview-box">'
            '<img src="{}" id="slider-image-preview" alt="Slider Preview" '
            'style="display:none;max-width:260px;max-height:180px;object-fit:cover;'
            'border-radius:12px;border:1px solid #ddd;">'
            '<span id="slider-image-placeholder" class="preview-placeholder">{}</span>'
            '</div>',
            "",
            "No Image Preview"
        )

    slider_image_preview.short_description = "Slider Preview"