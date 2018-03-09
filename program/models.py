from django.db import models
from accounts.models import User,Address,Driver
import datetime
# Create your models here.

class CarPath(models.Model):
    name    =   models.CharField(blank=False, max_length=120,null=True)
    lat = models.FloatField( blank=True, null=True)
    lon = models.FloatField( blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.name

class PackagingType(models.Model):
    name    =   models.CharField(blank=False, max_length=120,null=True)
    detail    =   models.CharField(blank=False, max_length=255,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.name

class Product(models.Model):
    sku                 = models.CharField(blank=False,max_length=120, editable=False)
    name                = models.CharField(blank=False,max_length=120)
    detail              = models.CharField(max_length=255,null=True)
    lot_number          = models.CharField(blank=False,max_length=120)
    mark                = models.CharField(max_length=120,null=True)
    type_product        = models.CharField(blank=False,max_length=120)
    type_packaging      = models.ForeignKey(PackagingType, on_delete=models.CASCADE)
    weight_product      = models.FloatField(blank=False)
    status              = models.IntegerField(default=1, editable=False)
    quantity            = models.IntegerField(default=1)
    total               = models.IntegerField(default=1)

    timestamp           = models.DateTimeField(auto_now_add=True)

    import_date         = models.DateTimeField()
    export_date         = models.DateTimeField(default=None, blank=True, null=True)
    manufacturing_date  = models.DateTimeField(default=None, blank=True, null=True)
    expire_date         = models.DateTimeField(default=None, blank=True, null=True)

    active              =   models.BooleanField(default=True)

    user                = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.sku

    def save(self, *args, **kwargs):
        if self.pk is None :
            today = datetime.date.today()
            today_string = today.strftime('%y%m%d')
            next_invoice_number = '01'
            last_invoice = Product.objects.filter(sku__startswith=today_string).order_by('sku').last()
            if last_invoice:
                last_invoice_number = int(last_invoice.sku[6:])
                next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
            self.sku = today_string + next_invoice_number
        super(Product, self).save(*args, **kwargs)
    @property
    def is_active(self):
        return  self.active

class Order(models.Model):

    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    address         = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    status          = models.IntegerField(default=1)
    #status 0 = cancel, status 1 = waiting for review, 2 = prepare for transport, 3 = product on the road 4 = complete
    def __str__(self):
        return  "%s" % self.pk

class OrderItem(models.Model):
    order           = models.ForeignKey(Order)
    product         = models.ForeignKey(Product)
    quantity        = models.IntegerField(default=1)
    def __str__(self):
        return "%s" % self.product.name

class OrderStatusChange(models.Model):
    order           = models.ForeignKey(Order)
    old_status      = models.IntegerField(default=1)
    new_status      = models.IntegerField(default=1)
    timestamp       = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.order.pk

class OrderTracking(models.Model):
    order_number    = models.CharField(blank=False,max_length=255)
    status          = models.IntegerField(default=1)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # status 0 = incative, 1 = active
    def __str__(self):
        return "%s" % self.pk

    def save(self, *args, **kwargs):
        if self.pk is None :
            today = datetime.date.today()
            today_string = today.strftime('%y%m%d')
            next_invoice_number = '01'
            last_invoice = OrderTracking.objects.filter(order_number__startswith=today_string).order_by('order_number').last()
            if last_invoice:
                last_invoice_number = int(last_invoice.order_number[6:])
                next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
            self.order_number = today_string + next_invoice_number
        super(OrderTracking, self).save(*args, **kwargs)

class TransportWithOrderTransection(models.Model):

    order           = models.ForeignKey(Order)
    driver          = models.ForeignKey(Driver)
    order_tracking  = models.ForeignKey(OrderTracking,null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    status          = models.IntegerField(default=1)
    #-2 arrive no success ,-1 = cancel, 0 = incative, 1 = active , 2 = arrive success
    def __str__(self):
        return "%s" % self.timestamp
class RecieveProductAddress(models.Model):
    detail          = models.CharField(blank=False,max_length=255)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    product_detail  = models.CharField(blank=False,max_length=255)

    name            = models.CharField(blank=False, max_length=120,null=True)
    tel             = models.CharField(max_length=120,null=True)
    status          = models.IntegerField(default=1)

    timestamp       = models.DateTimeField(auto_now_add=True)
    # status -2 = fail to recive product -1 = cancle  1 = waiting for review 2 = go for take product 3 take product success
    def __str__(self):
        return  self.detail
