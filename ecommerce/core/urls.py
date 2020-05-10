from django.urls import path
from django.conf.urls import url
from . import views as v

urlpatterns = [
    path('main', v.main, name='main'),
    path('ordersummary/', v.OrderSummaryView.as_view(), name='ordersummary'),
    path('', v.index, name='index'),
    path('product_detail/<int:id>/', v.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>', v.add_to_cart, name='add-to-cart'),
    path('update-cart/<int:id>', v.update_cart, name='update-cart'),
    path('remove-from-cart/<int:id>', v.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug:slug>', v.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]