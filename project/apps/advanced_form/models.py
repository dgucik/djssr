from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class ProductVolume(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='volume')
    volume = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.volume}"


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    info = models.TextField()

    def __str__(self):
        return f"{self.product.name} - Info"
    
