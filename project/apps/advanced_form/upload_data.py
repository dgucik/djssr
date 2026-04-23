from apps.advanced_form.models import ProductVolume


def upload_data():
    from apps.advanced_form.models import Product, ProductInfo, ProductVolume

    products = [
        Product(name="Product A", price=10),
        Product(name="Product B", price=20),
        Product(name="Product C", price=30),
    ]
    Product.objects.bulk_create(products)

    product_infos = [
        ProductInfo(product=products[0], info="Info for Product A"),
        ProductInfo(product=products[1], info="Info for Product B"),
        ProductInfo(product=products[2], info="Info for Product C"),
    ]
    ProductInfo.objects.bulk_create(product_infos)

    product_volumes = [
        ProductVolume(product=products[0], volume=10),
        ProductVolume(product=products[1], volume=20),
        ProductVolume(product=products[2], volume=30),
    ]
    ProductVolume.objects.bulk_create(product_volumes)