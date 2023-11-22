from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from products.models import Product


# Define choices for product status
STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('pickup', 'Pickup'),
    ('local_delivery', 'Local Delivery'),
    ('national_delivery', 'National Delivery'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=30,
        default="processing"
    )

    class Meta:
        verbose_name_plural = "Cart Orders"

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = CloudinaryField('product_image', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        # Use the URL of the Cloudinary image to display it in HTML
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)
