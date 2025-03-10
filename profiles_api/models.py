from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField  # ✅ Import CountryField for country selection
from django.apps import apps  # ✅ Lazy import to prevent circular imports


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None, country=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, country=country)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, country=None):
        """Create and return a superuser"""
        user = self.create_user(email, name, password, country)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, verbose_name="Full Name")
    country = CountryField(blank=True, null=True)  # ✅ Add country field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Retrieve full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name  # Use the `name` field as short_name

    def __str__(self):
        return f"{self.name} ({self.email})"


class HelpCategory(models.Model):
    """Categories for help articles"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, db_index=True)  # ✅ Faster lookups with db_index

    def __str__(self):
        return self.name


class HelpArticle(models.Model):
    """Help articles for the support section"""
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)  # ✅ Ensure fast queries
    content = models.TextField()  # Markdown supported
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Product categories with support for subcategories"""
    
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )  # ✅ Self-referencing field for subcategories

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_full_slug(self):
        """Get the full category path (e.g., mobile-phones)"""
        if self.parent:
            return f"{self.parent.get_full_slug()}/{self.slug}"
        return self.slug

    def __str__(self):
        """Display subcategories as Parent > Subcategory"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Product(models.Model):
    """Products available on Upfrica"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(default=list)  # Store images as a list of URLs
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )  # ✅ Added created_by field to track the user who created the product
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_country_code(self):
        """Detect user's country from request headers, query params, or geolocation"""
        if self.created_by and self.created_by.country:
            return self.created_by.country.code.lower()  # ✅ Get lowercase country code (e.g., 'gh', 'ng')
        return "global"

    def get_absolute_url(self):
        """Generate SEO-friendly URL: /gh/category-path/product-slug"""
        country_code = self.get_country_code()
        return f"/{country_code}/{self.category.get_full_slug()}/{self.slug}"

    def __str__(self):
        return self.title