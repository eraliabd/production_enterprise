from django.urls import path
from .views import ProductMaterialListAPIView, WarehouseView

urlpatterns = [
    path('', ProductMaterialListAPIView.as_view(), name='product_material'),
    path('warehouse/', WarehouseView.as_view(), name='warehouse')
]
