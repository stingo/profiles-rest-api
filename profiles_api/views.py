from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests
import logging  # ✅ Import logging for debugging

from .models import HelpArticle, HelpCategory, Product, Category
from .serializers import HelpArticleSerializer, HelpCategorySerializer, ProductSerializer

# ✅ Configure logging
logger = logging.getLogger(__name__)

# ✅ Function to detect user's country using Query Params or IP
def get_user_country(request):
    """
    Detect user country from:
    - URL query parameter (`?country=gh`)
    - IP address lookup (fallback)
    - Default: 'gh' (Ghana)
    """
    country = request.GET.get("country", "").strip().lower()
    if country:
        return country  # ✅ Return country if provided in the query string

    try:
        ip = request.META.get("HTTP_X_FORWARDED_FOR")  # ✅ Check if behind a proxy
        if ip:
            ip = ip.split(",")[0]  # ✅ Get first IP from the list
        else:
            ip = request.META.get("REMOTE_ADDR")  # ✅ Get direct IP

        if ip and ip != "127.0.0.1":  # ✅ Ignore localhost in development
            response = requests.get(f"https://ipapi.co/{ip}/json/")
            if response.status_code == 200:
                country_code = response.json().get("country_code", "").lower()
                if country_code:
                    return country_code  # ✅ Return detected country
    except Exception as e:
        logger.error(f"Error detecting country: {e}")  # ✅ Log errors

    return "gh"  # ✅ Default to Ghana if detection fails


# ✅ Help Category ViewSet
class HelpCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Help Categories"""
    queryset = HelpCategory.objects.all()
    serializer_class = HelpCategorySerializer


# ✅ Help Article ViewSet
class HelpArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for Help Articles"""
    queryset = HelpArticle.objects.all()
    serializer_class = HelpArticleSerializer
    lookup_field = "slug"


# ✅ API: Fetch all help articles
@api_view(["GET"])
def api_help_root(request):
    """
    Returns all help articles as JSON.
    Supports:
    - `/api/help/`
    - Query parameter `?search=keyword`
    """
    search_query = request.GET.get("search", "").strip().lower()
    articles = HelpArticle.objects.all()

    if search_query:
        articles = articles.filter(title__icontains=search_query)  # ✅ Case-insensitive search

    serialized_articles = HelpArticleSerializer(articles, many=True)

    # ✅ Ensure response is always an array
    return Response(serialized_articles.data if articles.exists() else [])


# ✅ API: Fetch a specific help article by slug (without `/articles/`)
@api_view(["GET"])
def api_help_detail(request, slug):
    """Retrieve a single help article by slug (without `/articles/`)."""
    try:
        article = HelpArticle.objects.get(slug=slug)
        serialized_article = HelpArticleSerializer(article)
        return Response(serialized_article.data)
    except HelpArticle.DoesNotExist:
        logger.warning(f"Help article not found: {slug}")
        return Response({"error": "Article not found"}, status=404)


# ✅ API: List all products filtered by user's country
class ProductListView(generics.ListAPIView):
    """API view to list all products filtered by user's detected country"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Return products based on user's detected country"""
        user_country = get_user_country(self.request)
        products = Product.objects.filter(created_by__country__iexact=user_country)

        if not products.exists():
            logger.info(f"No products found for country: {user_country}")

        return products


# ✅ API: Retrieve a product by SEO-friendly URL format (country + subcategory + slug)
class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a single product by country + subcategory + slug"""

    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_object(self):
        """Retrieve product based on country + subcategory + slug"""
        country = self.kwargs.get("country", "").strip().lower()
        subcategory = self.kwargs.get("subcategory", "").strip()
        slug = self.kwargs.get("slug", "").strip()

        if not country:
            country = get_user_country(self.request)  # ✅ Auto-detect if missing

        try:
            product = get_object_or_404(
                Product,
                slug=slug,
                created_by__country__iexact=country,
                category__slug=subcategory,
            )
            return product
        except Exception as e:
            logger.warning(f"Product not found: {slug} in {country}/{subcategory}")
            return Response({"error": "Product not found."}, status=404)


# ✅ API: List all products (function-based)
@api_view(["GET"])
def api_products(request, country=None):
    """
    Returns all products filtered by detected country.
    Supports:
    - URL (`/api/gh/products/`)
    - Query parameter (`?country=ng`)
    - IP lookup (fallback)
    """
    if not country:
        country = get_user_country(request)

    products = Product.objects.filter(created_by__country__iexact=country.lower())

    if not products.exists():
        logger.info(f"No products found for country: {country}")
        return Response({"message": "No products found for this country."}, status=404)

    serialized_products = ProductSerializer(products, many=True)
    return Response(serialized_products.data)


# ✅ API: Fetch product by SEO-friendly URL format (function-based)
@api_view(["GET"])
def api_product_detail(request, country=None, subcategory=None, slug=None):
    """
    Fetch a single product by country + subcategory + slug.
    Supports:
    - `/api/gh/mobile-phones/samsung-galaxy-s20/`
    - `/api/ng/electronics/macbook-pro-2023/`
    - Auto-detects country if missing
    """
    if not country:
        country = get_user_country(request)

    try:
        product = get_object_or_404(
            Product,
            slug=slug,
            created_by__country__iexact=country.lower(),
            category__slug=subcategory,
        )
        return Response(ProductSerializer(product).data)
    except Exception as e:
        logger.warning(f"Product not found for slug: {slug} in {country}/{subcategory}")
        return Response({"error": "Product not found."}, status=404)