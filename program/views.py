from django.shortcuts import render
from accounts.models import User,Address,Driver
from rest_framework import viewsets
from .serializers import UserSerializer, CarPathSerializer
from .models import CarPath
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, RecieveProductAddress,OrderStatusChange, TransportWithOrderTransection, OrderTracking
from django.forms.models import model_to_dict
from .forms import RecieveProductAddressForm,ProductForm
from django.core import serializers
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.db.models import Q


def staff_login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if not user.staff:
            return redirect('home')
        else:
            return function(request, *args, **kw)
    return wrapper


@login_required(login_url='home')
def program_page(request):
    if request.user.is_staff :

        return redirect('staff_view')

    else :
        list_items = []
        for order in Order.objects.filter(user__email=request.user.email,status = 1):
            for item in OrderItem.objects.filter(order__pk=order.pk):
                list_items.append(item)

        context = {
            "product_in_store"  : Product.objects.filter(user__pk = request.user.pk , active = 1),
            "list_order"        : Order.objects.filter(user__email=request.user.email, status = 1).order_by('-timestamp'),
            "list_items"        : list_items,
            "list_address"      : Address.objects.filter(user__pk=request.user.pk),
            "list_for_take"      : RecieveProductAddress.objects.filter(user__pk=request.user.pk,status = 1),
        }
        return render(request, 'program/program.html',context)

@login_required(login_url='home')
def order_transaction(request):
    print("hello")
    if request.method == "POST":

        print(request.user.address_pk)

        list_q = request.POST.getlist('quantity')
        list_id =  request.POST.getlist('product_select')
        print(list_q)
        print(list_id)
        try:
            address = Address.objects.get(pk = request.user.address_pk)

            if address == None :
                data = {
                    'error': 'no Address',
                    'status': '-3'
                }
                return JsonResponse(data)

            order = Order.objects.create(user = request.user,status = 1,address = address)

            if order == None :

                data = {
                    'error': 'cannot create order',
                    'status': '-2'
                }
                return JsonResponse(data)

            count = 0

            for id_product in list_id :

                product = Product.objects.get(pk = int(id_product))

                if product.quantity < int(list_q[count]) :
                    data = {
                        'error': 'quantity more than total product',
                        'status': '-1'
                    }
                    order.status = -1
                    return JsonResponse(data)
                product.quantity = product.quantity - int(list_q[count])
                if product.quantity == 0 :
                    product.active = 0

                product.save()

                orderItem = OrderItem.objects.create(order=order,product = product,quantity = list_q[count])
                count+=1

            data = {
                'success_with_order_id': order.pk
            }

            return JsonResponse(data)
        except ObjectDoesNotExist as inst:
            data = {
                'error': 'address not match',
                'status': '-3'
            }
            print(data)
            return JsonResponse(data)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)

            data = {
                'error': 'error',
                'status': '-1'
            }
            print(data)
            return JsonResponse(data)

@login_required(login_url='home')
def save_address(request):

    if request.method == "POST":
        address_detail = strip_tags(request.POST.get('detail'))

        try:
            address = Address.objects.create(user = request.user,detail = address_detail)

            user = User.objects.get(pk=request.user.pk)
            user.address_pk = address.pk
            user.save()

            html = ""

            html = html + '<div class="outer-address col-md-4"><div class="card card-body address_choose address-box" id="address-%s">' % address.pk
            html = html + '<div class="card-header"> ใช้ที่อยู่นี้จัดส่งสินค้า</div>'



            html = html + '<div class="address"><div class="card"><div class="card-body">'
            html = html + '<h5 class="card-title">ที่อยู่จัดส่ง %s </h5>' % Address.objects.filter(user = request.user).count()
            html = html + '<form>'

            html = html + '<div class="form-group">'
            html = html + '<div class="textwrapper">'
            html = html + '%s</div>' % address.detail
            html = html + '</div>'
            html = html + '<input type="hidden" name="address_pk" value="%s" >' % (address.pk)
            html = html + '</form> </div></div></div></div></div>'

            data = {
                'is_update' : 0 ,
                'address' : html

            }

            return JsonResponse(data)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)
            data = {
                'error': 'error'
            }
            return JsonResponse(data)

@csrf_exempt
@login_required(login_url='home')
def change_user_address(request):

    if request.method == "POST":
        if request.POST.get('address_pk') != None:
            try:
                user = User.objects.get(pk=request.user.pk)
                user.address_pk = request.POST.get('address_pk')
                user.save()


                data = {
                    'success' : 1 ,

                }

                return JsonResponse(data)
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)
                data = {
                    'error': 'error'
                }
                return JsonResponse(data)
        data = {
            'error': 'error'
        }
        return JsonResponse(data)

@login_required(login_url='home')
def add_address_page(request):
    return render(request, 'program/addaddress.html',{})

@login_required(login_url='home')
def reciever_product(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RecieveProductAddressForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            address_detail = form.cleaned_data['detail']
            product_detail = form.cleaned_data['product_detail']
            name = form.cleaned_data['name']
            tel = form.cleaned_data['tel']
            obj = RecieveProductAddress.objects.create(detail = address_detail,product_detail = product_detail, tel = tel, name = name,user = User.objects.get(pk = request.user.pk))
            return redirect('program_page')

    context = {
        'form'  : RecieveProductAddressForm
    }
    return render(request, 'program/reciever.html',context)


# staff page ...

@staff_login_required
def staff_view(request):
    status = 1
    if request.POST.get('status') != None:
        status = int(request.POST.get('status'))

    context = {
        "list_order"        : Order.objects.filter(status = status).order_by('-timestamp'),
        "status"            : status,
        "list_driver"       : Driver.objects.filter(active = 1)

    }

    return render(request, 'admin-program/program.html',context)

@staff_login_required
def manage_user(request):

    context = {
        "list_user"        : User.objects.filter(active=1).order_by('-timestamp'),

    }

    return render(request, 'admin-program/manage_user.html',context)

@staff_login_required
def product_view(request):

    if request.POST.get('search') != None:
        query_string = request.POST.get('search')
        print(query_string)
        context = {
            "list_product"        : Product.objects.filter(Q(active = 1),Q(name__icontains=query_string) | Q(user__email__icontains=query_string)).order_by('-timestamp'),
        }
    else :
        context = {
            "list_product"        : Product.objects.filter(active = 1).order_by('-timestamp'),
        }


    return render(request, 'admin-program/product.html',context)

@staff_login_required
def show_product_from_order(request):

    if request.method == "POST":
        if request.POST.get('id') != None:
            html = ""

            for product in OrderItem.objects.filter(order__pk=request.POST.get('id')) :
                html = html + '<tr class="odd gradeX">'
                html = html + '<td>%s</td>' % product.product.sku
                html = html + '<td>%s</td>' % product.product.name
                html = html + '<td>%s</td>' % product.quantity
                html = html + '</tr>'

            data = {
                'html':html
            }
            return JsonResponse(data)

        data = {
            'error': 'error'
        }
        return JsonResponse(data)

@staff_login_required
def update_order(request):

    if request.method == "POST":
        if (request.POST.get('order_id') != None) & (request.POST.get('update_status') != None):
            order = Order.objects.get(pk = request.POST.get('order_id'))
            order.status = int(request.POST.get('update_status'))
            order.save()
            order_update_status =  OrderStatusChange.objects.create(order=order,old_status = request.POST.get('status'), new_status = order.status)
            if order.status == 0 :
                order_items = OrderItem.objects.filter(order__pk = order.pk)

                for order_item in order_items :
                    product = Product.objects.get(pk = order_item.product.pk)
                    product.quantity = product.quantity + order_item.quantity
                    product.save()
            if order.status == 3 :
                print(request.POST.get('driver'))
                if (request.POST.get('driver') != None) :
                    driver = Driver.objects.get(pk = int(request.POST.get('driver')))
                    trans = TransportWithOrderTransection.objects.create(order=order,driver = driver)
                else :
                    print("Where is Driver?")

    status = 1
    if request.POST.get('status') != None:
        status = int(request.POST.get('status'))

    context = {
        "list_order"        : Order.objects.filter(status = status).order_by('-timestamp'),
        "status"            : status,
        "list_driver"       : Driver.objects.filter(active = 1)
    }

    return render(request, 'admin-program/program.html',context)

@staff_login_required
def update_user_company(request) :

    if request.method == "POST":
        if (request.POST.get('user_id') != None) & (request.POST.get('promote') != None):
            user = User.objects.get(pk = request.POST.get('user_id'))
            user.company = int(request.POST.get('promote'))
            user.save()

    context = {
        "list_user"        : User.objects.filter(active=1).order_by('-timestamp'),

    }
    return render(request, 'admin-program/manage_user.html',context)

@staff_login_required
def product_add(request) :
    if request.POST.get('search') != None:
        query_string = request.POST.get('search')
        context = {
            "list_recieve_address"        : RecieveProductAddress.objects.filter(Q(status=1),Q(detail__icontains=query_string) | Q(user__email__icontains=query_string)).order_by('-timestamp'),

        }

    else :
        context = {
            "list_recieve_address"        : RecieveProductAddress.objects.filter(status=1).order_by('-timestamp'),

        }

    return render(request, 'admin-program/product_add.html',context)

@staff_login_required
def product_add_item_page(request) :

    if request.method == 'POST':
        context = {
            'form': ProductForm
        }

        form = ProductForm(request.POST)
        # check whether it's valid:

        if form.is_valid() & (request.POST.get('user') != None) :
            fields = ['name', 'detail', 'lot_number','mark','type_product','type_packaging','weight_product','total','import_date','export_date','manufacturing_date','expire_date']

            name = form.cleaned_data['name']
            detail = form.cleaned_data['detail']
            lot_number = form.cleaned_data['lot_number']
            mark = form.cleaned_data['mark']
            type_product = form.cleaned_data['type_product']
            type_packaging = form.cleaned_data['type_packaging']
            weight_product = form.cleaned_data['weight_product']
            total = form.cleaned_data['total']
            import_date = form.cleaned_data['import_date']
            export_date = form.cleaned_data['export_date']
            manufacturing_date = form.cleaned_data['manufacturing_date']
            expire_date = form.cleaned_data['expire_date']


            obj = Product.objects.create(name = name,detail = detail, lot_number = lot_number,
             mark = mark,type_product = type_product,type_packaging = type_packaging,weight_product = weight_product,
             total = total,quantity = total,import_date = import_date,export_date = export_date,manufacturing_date = manufacturing_date,
             expire_date = expire_date,user = User.objects.get(pk = int(request.POST.get('user'))))

        if request.POST.get('recieve_id') != None:
            recieve = RecieveProductAddress.objects.get(pk=request.POST.get('recieve_id'))
            user = User.objects.get(pk = recieve.user.pk)
            context = {
                "list_product"        : Product.objects.filter(active=1,user__pk = user.pk).order_by('-timestamp'),
                "user_owner"          : user,
                "recieve"          : recieve,
                'form': ProductForm,
            }

        return render(request, 'admin-program/add_item_page.html',context)

    context = {
        'form': ProductForm
    }

    return render(request, 'admin-program/add_item_page.html',context)

@staff_login_required
def request_inactive(request) :
    if request.method == 'POST':
        if request.POST.get('recieve_id') != None:
            recieve = RecieveProductAddress.objects.get(pk=request.POST.get('recieve_id'))
            recieve.status = 0
            recieve.save()
    return redirect('product_add')

@staff_login_required
def product_inactive(request) :
    if request.method == 'POST':
        if request.POST.get('product_id') != None:
            product = Product.objects.get(pk=request.POST.get('product_id'))
            product.active = 0
            product.save()
            data = {
                'success':'update success'
            }
            return JsonResponse(data)

    data = {
        'error':'update error'
    }
    return JsonResponse(data)

@staff_login_required
def launch_truck_page(request) :

    context = {
        "list_order"         : TransportWithOrderTransection.objects.filter(status=1).order_by('-timestamp'),
        "list_order_run"         : TransportWithOrderTransection.objects.filter(status=2).order_by('-timestamp'),
        "list_driver"         : Driver.objects.filter(active=1).order_by('-timestamp'),
        "list_ordertracking"         : OrderTracking.objects.filter(status=1).order_by('-timestamp')
    }

    return render(request, 'admin-program/create_order_tracking.html',context)

@staff_login_required
def launch_truck(request) :

    if request.method == 'POST':

        if request.POST.getlist('trans_id') != None:
            ordertracking = OrderTracking.objects.create(status = 1)
            if ordertracking != None :
                for trans_id in request.POST.getlist('trans_id') :
                    t = TransportWithOrderTransection.objects.get(pk = trans_id )
                    t.status = 2
                    t.order_tracking = ordertracking
                    t.save()

    return redirect('launch_truck_page')

@staff_login_required
def complete_launch(request) :

    if request.method == 'POST':

        if request.POST.get('ordertracking_id') != None:
            print('awefewfewa')
            ordertracking = OrderTracking.objects.get(pk = int(request.POST.get('ordertracking_id')))
            ordertracking.status = 2
            ordertracking.save()
            for trans in TransportWithOrderTransection.objects.filter(order_tracking__pk = ordertracking.pk) :
                trans.status = 2
                trans.save()

                order = Order.objects.get(pk = trans.order.pk)
                order.status = 4
                order.save()

    return redirect('launch_truck_page')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-timestamp')
    serializer_class = UserSerializer

class CarPathViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CarPath.objects.all().order_by('-timestamp')
    serializer_class = CarPathSerializer
