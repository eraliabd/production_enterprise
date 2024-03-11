import json

from rest_framework import generics
from rest_framework.response import Response
from .models import ProductMaterial, Product, Warehouse, Material
from .serializers import (
    ProductMaterialSerializer, FilterSerializer
)


class ProductMaterialListAPIView(generics.ListAPIView):
    queryset = ProductMaterial.objects.all()
    serializer_class = FilterSerializer


class WarehouseView(generics.ListAPIView):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer

    def get_queryset(self):
        result = []
        material_data = ProductMaterial.objects.all().order_by('-id')
        serializer_data = ProductMaterialSerializer(material_data, many=True).data

        for product_material in serializer_data:
            product_name = product_material.get('product')['product_name']
            product_qty = product_material.get('quantity')
            materials = product_material.get('material')

            product_materials = []
            for material in materials:
                warehouses = Warehouse.objects.filter(material=material['id'])
                material_name = material.get('material_name')

                for warehouse in warehouses:
                    warehouse_id = warehouse.id
                    price = warehouse.price if warehouse.price is not None else None
                    product_materials.append({
                        "warehouse_id": warehouse_id,
                        "material_name": material_name,
                        "qty": warehouse.remainder,
                        "price": price
                    })

            result.append({
                "product_name": product_name,
                "product_qty": product_qty,
                "product_materials": product_materials
            })

        return result

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({"result": queryset})
