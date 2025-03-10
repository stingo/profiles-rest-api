from rest_framework import serializers
from .models import HelpCategory, HelpArticle, Product, Category

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class HelpCategorySerializer(serializers.ModelSerializer):
    """Serializer for Help Categories"""

    class Meta:
        model = HelpCategory
        fields = "__all__"

class HelpArticleSerializer(serializers.ModelSerializer):
    """Serializer for Help Articles"""
    category = serializers.PrimaryKeyRelatedField(queryset=HelpCategory.objects.all())

    class Meta:
        model = HelpArticle
        fields = "__all__"

# ✅ Updated ProductSerializer with category hierarchy, proper country serialization, and SEO-friendly URL
class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""

    created_by_name = serializers.SerializerMethodField()
    created_by_country = serializers.SerializerMethodField()
    category_path = serializers.SerializerMethodField()  # ✅ Get full category path
    product_url = serializers.SerializerMethodField()  # ✅ Generate SEO-friendly URL

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "images",
            "created_at",
            "updated_at",
            "category_path",      # ✅ Show category hierarchy
            "product_url",        # ✅ Include SEO-friendly URL
            "created_by_name",     # ✅ Show creator's name
            "created_by_country",  # ✅ Show creator's country as a string
        ]

    def get_created_by_name(self, obj):
        """Get creator's name or return 'Unknown' if missing"""
        return obj.created_by.name if obj.created_by else "Unknown"

    def get_created_by_country(self, obj):
        """Get creator's country as a string or return 'Unknown' if missing"""
        return str(obj.created_by.country).lower() if obj.created_by and obj.created_by.country else "unknown"

    def get_category_path(self, obj):
        """Return full category path as 'Parent > Subcategory' (e.g., 'Agriculture > Agricultural Equipment')"""
        category = obj.category
        if not category:
            return "Uncategorized"

        path = []
        while category:
            path.insert(0, category.name)
            category = category.parent  # ✅ Traverse up the category tree

        return " > ".join(path)  # ✅ Join categories with " > "

    def get_product_url(self, obj):
        """Generate SEO-friendly product URL"""
        country_code = self.get_created_by_country(obj)

        # ✅ Ensure we always have a category slug for SEO URLs
        if obj.category and obj.category.parent:
            subcategory_slug = obj.category.slug  # ✅ Subcategory (e.g., 'mobile-phones')
        elif obj.category:
            subcategory_slug = obj.category.slug  # ✅ Fallback to main category if no parent
        else:
            subcategory_slug = "uncategorized"  # ✅ Default if no category assigned

        # ✅ Final SEO-friendly URL structure
        return f"/{country_code}/{subcategory_slug}/{obj.slug}"