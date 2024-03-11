from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_code = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Material(models.Model):
    material_name = models.CharField(max_length=250)

    def __str__(self):
        return self.material_name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    material = models.ManyToManyField(Material, related_name='materials')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product} {self.quantity} ta"


class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.material} {self.remainder} {self.price}"
