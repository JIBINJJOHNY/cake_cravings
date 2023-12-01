from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from decimal import Decimal
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Category Name',
        help_text='Format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Category Slug',
        help_text='Format: required, max_length=150'
    )
    is_active = models.BooleanField(default=False)
    image = CloudinaryField(folder='category', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.name

class Tag(models.Model):
    """Cake Cravings Tag model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag Name',
        help_text='The name of the tag (e.g., "Offer 10%", "New", "International Shipping").'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag Slug',
        help_text='A slugified version of the tag name (e.g., "offer-10", "new", "international-shipping").'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is Active',
        help_text='Is this tag currently active and displayed on the website?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
        help_text='The date and time when this tag was created.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
        help_text='The date and time when this tag was last updated.'
    )

    class Meta:
        """Meta class for Cake Cravings Tag model"""
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        """String representation of Cake Cravings Tag model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_tags(cls):
        """Get active tags"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_tags(cls):
        """Get not active tags"""
        return cls.objects.filter(is_active=False)

class Discount(models.Model):
    percentage = models.PositiveIntegerField(help_text='Discount percentage')
    start_date = models.DateField(help_text='Start date of the discount')
    end_date = models.DateField(help_text='End date of the discount')
    is_active = models.BooleanField(default=True, help_text='Is the discount currently active?')

    def is_valid(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.is_active

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small (18cm - 6 portions)'),
        ('M', 'Medium (26cm - 12 portions)'),
        ('L', 'Large (36cm - 25 portions)'),
    ]

    AVAILABILITY_CHOICES = [
        ('out_of_stock', 'Out of Stock'),
        ('upcoming', 'Upcoming'),
        ('in_stock', 'In Stock'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)

        # Only adjust price based on size if the category is 'cakes'
        if self.category.name.lower() == 'cakes' and self.size:
            if self.size == 'S':
                self.price = Decimal('30.0')
            elif self.size == 'M':
                self.price = Decimal('45.0')
            elif self.size == 'L':
                self.price = Decimal('80.0')

        # Check if a discount is applicable
        if self.discount_price and self.discount_price.is_valid():
            discount_amount = (self.discount_price.percentage / Decimal(100)) * self.price
            self.price -= discount_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Product',
        help_text='The associated product for this image.'
    )
    image = CloudinaryField(
        'image', 
        folder='product_images',
        null=True,
        blank=True,
    )
    alt_text = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='Alt text',
        help_text='Descriptive text for the image.'
    )
    default_image = models.BooleanField(
        default=False,
        verbose_name='Default Image',
        help_text='Is this the default image for the product?'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is Active',
        help_text='Is this image currently active?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
        help_text='The date and time when this image was created.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
        help_text='The date and time when this image was last updated.'
    )

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['product']

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return 'static/images/default_image.png'

    @classmethod
    def get_active_product_images(cls):
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_product_images(cls):
        return cls.objects.filter(is_active=False)

    def save(self, *args, **kwargs):
        if self.default_image:
            for image in self.product.images.all().exclude(id=self.id):
                image.default_image = False
                image.save()

        super().save(*args, **kwargs)
