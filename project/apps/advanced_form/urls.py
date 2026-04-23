from django.urls import path

from apps.advanced_form.views import ProductBatchUpdateView, ProductPageView

app_name = 'advanced_form'

urlpatterns = [
    path('', ProductPageView.as_view(), name='index'),
    path('batch-update/', ProductBatchUpdateView.as_view(), name='batch_update'),
]
