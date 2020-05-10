from django.contrib import admin
# Register your models here.
from .models import products ,Image ,OrderItem, Order, Coupon, Variation
from .models import category

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title','description']
    date_hierarchy = 'timestamp'
    list_display = ['__str__','title', 'active', 'timestamp','updated','Category','default_price']
    list_editable = ['active','default_price']
    list_filter =['active']
    readonly_fields = ['updated','timestamp']
    prepopulated_fields = {"slug": ("title",)}



    class Meta:
        model= products

admin.site.register(products, ProductAdmin)


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ['product', ]
admin.site.register(Image, ImageAdmin)



class categoryAdmin(admin.ModelAdmin):
            search_fields = ['category_title', 'category_description']
            list_display = ['category_title', 'category_description']
            prepopulated_fields = {"category_slug": ("category_title",)}
            class Meta:
                model = category

admin.site.register(category,categoryAdmin )





class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]



admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)
admin.site.register(Variation)