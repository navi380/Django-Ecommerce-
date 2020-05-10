from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Q


class category(models.Model):
    category_title = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to="category")
    category_description = models.TextField()
    category_slug = models.SlugField(max_length=200)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_title


class ProductQuerySet(models.query.QuerySet):

  def active(self):
    return self.filter(active=True)

  def featured(self):
    return self.filter(featured=True, active=True)

  def search(self, query):
    lookups = (Q(title__icontains=query) |
               Q(description__icontains=query) |
               Q(default_price__icontains=query) |
               Q(slug__icontains=query)
    )
    return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


# Create your models here.
class products(models.Model):
    title= models.CharField(max_length=120)
    Category = models.ForeignKey(category, blank=True, on_delete=models.CASCADE, related_name="product")
    slug= models.SlugField(blank=True, unique=True)
    description= models.TextField()
    featured= models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    default_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    discount_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00 ,blank=True, null=True)
    default_img =models.ImageField(upload_to="static/img/")

    objects = ProductManager()

    class Meta:
        db_table = 'products'
        index_together = (('id', 'slug'),)

#product title will shown in admin method below
    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(products,on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="static/img/")

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager ,self).filter(active = True)
    def sizes(self):
        return self.all().filter(category='size')
    def colors(self):
        return self.all().filter(category='color')


Var_CHOICES = (
    ('size', 'size'),
    ('color', 'color'),
)
class Variation(models.Model):
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    category = models.CharField(choices=Var_CHOICES, max_length=150, blank=True)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    active= models.BooleanField(default=True)

    objects = VariationManager()
    def __str__(self):
        return self.title




class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    variations = models.ManyToManyField(Variation, blank=True )
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.default_price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.default_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, blank=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null= True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



class stock(models.Model):
    product = models.OneToOneField(
        products,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    #product = models.ForeignKey(products, on_delete=models.CASCADE)
    #Product_Size = models.ForeignKey(product_size, on_delete=models.CASCADE , blank=True, null= True)
    #Product_Color = models.ForeignKey(product_color, on_delete=models.CASCADE,  blank=True, null= True)
    date = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)

    #def __int__(self):
        #return self.id