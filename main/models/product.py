from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
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

    image = models.ImageField(upload_to="products/featured/")

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        editable=False
    )

    description = CKEditor5Field("Description", config_name="default")

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.discount_percent > 0:
            discount_amount = (self.original_price * Decimal(self.discount_percent)) / Decimal("100")
            self.final_price = self.original_price - discount_amount
        else:
            self.final_price = self.original_price

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product.title} - Image"