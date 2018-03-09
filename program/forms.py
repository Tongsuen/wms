from django import forms
from django.forms import ModelForm, Textarea
from .models import RecieveProductAddress,Product
from django.utils.translation import ugettext_lazy as _

class OrderChoose(forms.Form):
    product_select = forms.BooleanField(required=False)
    quantity = forms.IntegerField(required=False)

class RecieveProductAddressForm(ModelForm):
    class Meta:
        model = RecieveProductAddress
        fields = ['detail', 'product_detail', 'name','tel']
        widgets = {
            'detail': Textarea(attrs={ 'rows':5}),
            'product_detail': Textarea(attrs={ 'rows':5}),
        }
        labels = {
            "detail": _("ที่อยู่สำหรับรับสินค้า"),
            "product_detail": _("รายระเอียดสินค้า"),
            "name": _("ชื่อผู้รับสินค้า"),
            "tel": _("เบอร์โทรที่สามารถติดต่อได้"),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'detail', 'lot_number','mark','type_product','type_packaging','weight_product','total','import_date','export_date','manufacturing_date','expire_date']
        widgets = {
            'detail': Textarea(attrs={ 'rows':3}),

            'import_date': forms.DateInput(attrs={'class':'datetime-input'}),
            'export_date': forms.DateInput(attrs={'class':'datetime-input'}),
            'manufacturing_date': forms.DateInput(attrs={'class':'datetime-input'}),
            'expire_date': forms.DateInput(attrs={'class':'datetime-input'}),
        }
        labels = {
            "name": _("ชื่อสินค้า"),
            "detail": _("รายระเอียดสินค้า"),
            "lot_number": _("LOT NUMBER"),
            "mark": _("remark"),
            "type_product": _("ประเภทสินค้า"),
            "type_packaging": _("ประเภทบรรจุภัณฑ์"),
            "weight_product": _("น้ำหนักต่อชิ้นเป็นกิโลกรัม"),
            "total": _("จำนวนสินค้า"),
        }
