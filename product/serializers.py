from rest_framework import serializers

from .models import Product, Material, ProductMaterial, Warehouse


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_code')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'material_name')


class ProductMaterialSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    material = MaterialSerializer(many=True)

    class Meta:
        model = ProductMaterial
        fields = ('id', 'product', 'material', 'quantity')


class WarehouseSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(source='id')
    material_name = serializers.CharField(max_length=250, source='material')
    qty = serializers.IntegerField(source='remainder')

    class Meta:
        model = Warehouse
        fields = ('warehouse_id', 'material_name', 'qty', 'price')


class FilterSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product', max_length=250)
    product_qty = serializers.IntegerField(source='quantity')
    product_materials = serializers.SerializerMethodField(source='materials')

    class Meta:
        model = ProductMaterial
        fields = ('product_name', 'product_qty', 'product_materials')

    def get_product_materials(self, obj):
        warehouses = obj.material.all().values_list('warehouse', flat=True)
        warehouse_instances = Warehouse.objects.filter(material_id__in=warehouses)
        serializer = WarehouseSerializer(instance=warehouse_instances, many=True)
        return serializer.data
