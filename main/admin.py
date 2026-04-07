from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Slider


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

    readonly_fields = ("image_preview",)

    fields = (
        "title",
        "slug",
        "image",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj and obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="width:120px;height:120px;object-fit:cover;border-radius:12px;border:1px solid #ddd;box-shadow:0 4px 12px rgba(0,0,0,0.08);" />',
                obj.image.url
            )
        return "No Image Preview"

    image_preview.short_description = "Preview"

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:10px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = "Image"


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    min_num = 0
    fields = ("image", "image_preview")
    readonly_fields = ("image_preview",)
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"

    class Media:
        js = ("js/admin_image_preview.js",)

    def image_preview(self, obj):
        if obj and obj.pk and obj.image:
            return format_html(
                """
                <div class="admin-inline-preview-box">
                    <img src="{}" class="admin-live-preview inline-image-preview" alt="Preview">
                </div>
                """,
                obj.image.url
            )
        return mark_safe(
            """
            <div class="admin-inline-preview-box">
                <img src="" class="admin-live-preview inline-image-preview" alt="Preview" style="display:none;">
                <span class="preview-placeholder">No Preview</span>
            </div>
            """
        )

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "title",
        "category",
        "original_price",
        "discount_percent",
        "final_price",
        "created_at",
    )
    list_filter = ("category",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("main_image_preview", "final_price")

    fields = (
        "title",
        "slug",
        "category",
        "image",
        "main_image_preview",
        "original_price",
        "discount_percent",
        "description",
        "final_price",
    )

    inlines = [ProductImageInline]

    class Media:
        js = ("js/admin_image_preview.js",)

    def main_image_preview(self, obj):
        if obj and obj.pk and obj.image:
            return format_html(
                """
                <div class="admin-main-preview-box">
                    <img src="{}" id="main-image-preview" alt="Main Preview">
                </div>
                """,
                obj.image.url
            )
        return mark_safe(
            """
            <div class="admin-main-preview-box">
                <img src="" id="main-image-preview" alt="Main Preview" style="display:none;">
                <span id="main-image-placeholder" class="preview-placeholder">No Image Preview</span>
            </div>
            """
        )

    main_image_preview.short_description = "Main Image Preview"

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:10px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = "Image"


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("slider_image_preview", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    readonly_fields = ("slider_image_preview",)

    fields = (
        "title",
        "slider_image_preview",
        "image",
        "order",
        "is_active",
    )

    class Media:
        js = ("js/admin_image_preview.js",)

    def slider_image_preview(self, obj):
        if obj and obj.pk and obj.image:
            return format_html(
                """
                <div class="admin-slider-preview-box">
                    <img src="{}" id="slider-image-preview" alt="Slider Preview">
                </div>
                """,
                obj.image.url
            )
        return mark_safe(
            """
            <div class="admin-slider-preview-box">
                <img src="" id="slider-image-preview" alt="Slider Preview" style="display:none;">
                <span id="slider-image-placeholder" class="preview-placeholder">No Image Preview</span>
            </div>
            """
        )

    slider_image_preview.short_description = "Slider Preview"


admin.site.site_header = "Mega Sewa Global Admin Panel"
admin.site.site_title = "Mega Sewa Global Admin"
admin.site.index_title = "Welcome to Mega Sewa Global Dashboard"