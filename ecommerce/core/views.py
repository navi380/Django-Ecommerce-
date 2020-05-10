from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import products,category ,Order,OrderItem,Variation , stock
# Create your views here.


def main(request):
    cat = category.objects.all()
    obj = products.objects.all()

    context = {
        'object': obj,
        'visible_list': obj[:10],
        'hidden_list': obj[6:],
        'cat': cat,

    }
    return render(request,'crausal check.html',context)
def product_detail(request, id ):

    produc = get_object_or_404(products, id=id )

    context = {
        'product': produc,

    }
    return render(request, 'itemdetail.html', context)


def index(request):
    return render(request, 'index.html')


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'ordersummary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("ordersummary")

@login_required(login_url='/login')

def update_cart(request, id):
    item = get_object_or_404(products, id=id)
    order_item = OrderItem.objects.get(item=item , user= request.user ,ordered=False)
    order_item.quantity += 1
    order_item.save()
    messages.info(request, "This item quantity was updated.")
    return redirect('ordersummary')





@login_required(login_url='/login')
def add_to_cart(request, id):
    item = get_object_or_404(products, id=id)
    product_var = []
    v = None
    if request.method == "POST":
        for i in request.POST:
            key = i
            val = request.POST[key]
            try:
                v = Variation.objects.get(product = item ,category__iexact =key , title__iexact =val)
                product_var.append(v)
            except:
                pass
    print(product_var)
    order_item = OrderItem.objects.create(
            item=item, user=request.user, ordered=False)
    # print(order_item)==admin
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    #print(order_qs) ==return queryset[]
    # if there is a order
    if order_qs.exists():
        order = order_qs[0]
        order_item.variations.add(*product_var)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('ordersummary')
    # if there is no order..first time order and first item
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order_item.variations.add(*product_var)
        order.items.add(order_item)
    return redirect('ordersummary')


@login_required(login_url='/login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        order_item = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )[0]
        if order_item.quantity > 1:
            order_item.quantity -= 1
            #st.quantity += 1
            #st.save()
            order_item.save()
        else:
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "The item quantity was updated")
        return redirect('ordersummary')
    else:
        messages.info(request, "This item was not in your cart")
        return redirect('ordersummary')


@login_required(login_url='/login')
def remove_from_cart(request, id):
    item = get_object_or_404(products, id=id)

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()

            messages.info(request, "This item was removed from your cart.")
            return redirect("ordersummary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('ordersummary')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('ordersummary')
