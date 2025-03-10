from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles_api.models import UserProfile, HelpCategory, HelpArticle, Category, Product

# ✅ Custom User Admin Configuration
class CustomUserAdmin(UserAdmin):
    """Customize Django Admin for UserProfile"""

    model = UserProfile
    list_display = ("email", "name", "country", "is_staff", "is_active")  # ✅ Display country
    ordering = ("email",)
    search_fields = ("email", "name", "country")  # ✅ Allow search by country
    list_filter = ("is_staff", "is_active", "country")  # ✅ Filter by country

    # ✅ Override UserAdmin fields
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "country")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    # ✅ Add fields for user creation in admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "country", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

    filter_horizontal = ()  # ✅ Remove groups/permissions if not needed


# ✅ Custom Admin for Category with Parent-Child Structure
class CategoryAdmin(admin.ModelAdmin):
    """Admin customization for category hierarchy"""
    
    list_display = ("name", "parent")  # ✅ Show parent category
    search_fields = ("name",)
    list_filter = ("parent",)  # ✅ Filter by parent category
    
    def get_queryset(self, request):
        """Ensure categories are displayed in a structured order"""
        return super().get_queryset(request).order_by("parent__name", "name")


# ✅ Register Models in Django Admin
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(HelpCategory)
admin.site.register(HelpArticle)
admin.site.register(Category, CategoryAdmin)  # ✅ Use CategoryAdmin for hierarchy
admin.site.register(Product)