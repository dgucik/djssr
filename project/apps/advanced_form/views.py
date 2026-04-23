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

        # Bootstraps Alpine.js state — keyed by PK string so JS can do O(1) lookups.
        products_json = {}
        for p in products:
            # OneToOne reverse accessor raises DoesNotExist (not None) when missing.
            try:
                vol = str(p.volume.volume)
            except ProductVolume.DoesNotExist:
                vol = ''
            products_json[str(p.pk)] = {'name': p.name, 'volume': vol}

        # Separate dict so the two table cards (Products & Info) share one JS state object.
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

        # Maps temp frontend key → real DB IDs so the client can swap them out.
        created = {}

        # Pass 1: insert rows added in the current session.
        # Frontend uses "new_<n>" prefix as a sentinel for rows without a real PK yet.
        for key, fields in data.get('products', {}).items():
            if not key.startswith('new_'):
                continue
            product = Product.objects.create(
                name=fields.get('name', ''),
                price=0,
                description='',
            )
            volume_val = str(fields.get('volume', '')).strip()
            if volume_val:
                ProductVolume.objects.create(product=product, volume=volume_val)
            # Frontend pairs each product key with "<key>_info" for its ProductInfo entry.
            info_key = key + '_info'
            info_data = data.get('infos', {}).get(info_key, {})
            info = ProductInfo.objects.create(
                product=product,
                info=info_data.get('info', ''),
            )
            created[key] = {'product_id': product.pk, 'info_id': info.pk}

        # Pass 2: update existing products (skip new_ rows already handled above).
        for pk_str, fields in data.get('products', {}).items():
            if pk_str.startswith('new_'):
                continue
            product = get_object_or_404(Product, pk=int(pk_str))
            product.name = fields.get('name', product.name)
            product.save()
            volume_val = str(fields.get('volume', '')).strip()
            if volume_val:
                ProductVolume.objects.update_or_create(
                    product=product,
                    defaults={'volume': volume_val},
                )

        for pk_str, fields in data.get('infos', {}).items():
            if pk_str.startswith('new_'):
                continue
            info = get_object_or_404(ProductInfo, pk=int(pk_str))
            info.info = fields.get('info', info.info)
            info.save()

        return JsonResponse({'status': 'ok', 'created': created})
