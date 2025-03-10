# Import necessary views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import views
from .views import (
    HelpCategoryViewSet,
    HelpArticleViewSet,
    ProductListView,
    ProductDetailView,
    api_products,
    api_product_detail,
    api_help_detail,  # ✅ Import the function for single article retrieval
    api_help_root,    # ✅ Import the function for listing all help articles
)
# ✅ Initialize router for admin API access
router = DefaultRouter()
router.register("help/categories", HelpCategoryViewSet, basename="help-category")
router.register("help/articles", HelpArticleViewSet, basename="help-article")  # Keep this for admin API access

# ✅ Define URL patterns
urlpatterns = [
    # ✅ Fetch all help articles (supports search via `?search=keyword`)
    path("help/", api_help_root, name="help-root"),

    # ✅ Fetch a single help article by slug (without `/articles/`)
    path("help/<str:slug>/", api_help_detail, name="help-article-detail"),

    # ✅ Country-based product listing (e.g., `/api/gh/products/`)
    path("<str:country>/products/", api_products, name="products-list"),

    # ✅ SEO-friendly product details: `/api/<country>/<subcategory>/<product-slug>/`
    path("<str:country>/<str:subcategory>/<str:slug>/", ProductDetailView.as_view(), name="product-detail-seo"),

    # ✅ Include DRF router URLs for admin API access
    path("", include(router.urls)),
]