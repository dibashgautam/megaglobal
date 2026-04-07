from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from .category import Category


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    # Main / Featured Image (Required)
    image = models.ImageField(upload_to="products/featured/")

    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    description = CKEditor5Field("Description", config_name="default")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.discount_percent > 0:
            discount_amount = (self.original_price * self.discount_percent) / 100
            self.final_price = self.original_price - discount_amount
        else:
            self.final_price = self.original_price

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


# 🔥 Multiple Gallery Images Model
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product.title} - Image"