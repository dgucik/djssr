import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from apps.advanced_form.models import Product, ProductInfo, ProductVolume


class ProductPageView(TemplateView):
    template_name = 'advanced_form/product_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = list(Product.objects.prefetch_related('volume', 'productinfo_set'))

        products_json = {}
        for p in products:
            try:
                vol = str(p.volume.volume)
            except ProductVolume.DoesNotExist:
                vol = ''
            products_json[str(p.pk)] = {'name': p.name, 'volume': vol}

        infos_json = {}
        for p in products:
            for info in p.productinfo_set.all():
                infos_json[str(info.pk)] = {'info': info.info}

        context['products'] = products
        context['products_json'] = json.dumps(products_json)
        context['infos_json'] = json.dumps(infos_json)
        return context


class ProductBatchUpdateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        for pk_str, fields in data.get('products', {}).items():
            product = get_object_or_404(Product, pk=int(pk_str))
            product.name = fields.get('name', product.name)
            product.save()
            volume_val = fields.get('volume', '').strip()
            if volume_val:
                ProductVolume.objects.update_or_create(
                    product=product,
                    defaults={'volume': volume_val},
                )

        for pk_str, fields in data.get('infos', {}).items():
            info = get_object_or_404(ProductInfo, pk=int(pk_str))
            info.info = fields.get('info', info.info)
            info.save()

        return JsonResponse({'status': 'ok'})
