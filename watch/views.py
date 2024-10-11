from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from watch.forms import SiginForm,SignupForm,UserProfileForm
from django.contrib import messages
from watch.models import Project,WishListItems,OrderSummary,UserProfile
from django.db.models import Sum,Aggregate
from django.utils.decorators import method_decorator
from django.views.generic import ListView



class SignUpView(View):
    def get(self,request,*args,**kwargs):

        form_instance=SignupForm()

        return render(request,"register.html",{"register":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignupForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            messages.success(request,"successfuly created account")
            return redirect("login")

        else:
            return render(request,"register.html",{"register":form_instance})

class SignInView(View):
    def get(self,request,*args,**kwargs):

        form_instance=SiginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SiginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_obj=authenticate(**data)

            if user_obj:

                login(request,user_obj)

                messages.success(request,"successfully login")
                

                return redirect("home")
            else:
                return render(request,"login.html",{"form":form_instance})
            
class SignOutView(View):
    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("login")
    

class HomeView(View):

    def get(self,request,*args,**kwargs):

        project_object=Project.objects.all()


        return render(request,"home.html",{"project":project_object})
    


class ProjectDetailView(View):

    def get(self,request,*args,**kwargs):
         
        id=kwargs.get("pk")


        project_object=Project.objects.get(id=id)

        return render(request,"project_detail.html",{"project":project_object})
    

class AddtoCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")


        project_obj=Project.objects.get(id=id)

        WishListItems.objects.create(project_object=project_obj,wishlist_object=request.user.basket)

        return render(request,"project_detail.html",{"project":project_obj})
    

class WishListView(View):

    def get(self,request,*args,**kwargs):

        wishlist_obj=WishListItems.objects.filter(is_order_placed=False)

        total=request.user.basket.basket_items.filter(is_order_placed=False).aggregate(total=Sum("project_object__price")).get("total")


        return render(request,"wishlist_items.html",{"cartitems":wishlist_obj,"total":total})
    
class ProjectRemoveView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItems.objects.get(id=id).delete()
       

        return redirect("wish-list")
    
class UserProfileUpdateView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        obj=UserProfile.objects.get(id=id)

        form_instance=UserProfileForm(instance=obj)

        return render(request,"profile_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        user_obj=UserProfile.objects.get(id=id)

        form_instance=UserProfileForm(request.POST,files=request.FILES,instance=user_obj)

        if form_instance.is_valid():
            form_instance.instance.user_object=request.user

            form_instance.save()

            return redirect("home")
        else:
            return render(request,"profile_edit.html",{"form":form_instance})


KEY_SECRET="Jyysw17HuOHdTa2LhaOm341q"

KEY_ID="rzp_test_V8m3fmZMilZ1O4"

import razorpay
class AddressAddView(View):
    def get(self,request,*args,**kwargs):

        return render(request,"details_add.html")
    
    def post(self,request,*args,**kwargs):

        name=request.POST.get("name")

        address=request.POST.get("address")

        phone=request.POST.get("phone")

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        t=request.user.basket.basket_items.filter(is_order_placed=False).aggregate(total=Sum("project_object__price")).get("total")

        total=t*100

        data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        #create order object

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)



    
           
        order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get("id"),total=t,name=name,address=address,phone=phone)
           
    

        for ci in cart_items:

            order_summary_obj.project_objects.add(ci.project_object)

            print("==========================",order_summary_obj)

        order_summary_obj.save()
            
        

        print(payment)

        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }


        return render(request,"checkout.html",{"context":context})
    







from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")

class PaymentVerification(View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        order_summary_obj=OrderSummary.objects.get(order_id=request.POST.get("razorpay_order_id"))

        login(request,order_summary_obj.user_object)

        # 'razorpay_payment_id': ['pay_Osc4W3SzwsS9D4'], 'razorpay_order_id': ['order_Osc45PLWmmuS2r'], 'razorpay_signature': ['0ddd337bace49384729e5bb28dcb3b115e6b41df29bd0d4e6ef189d81748931d'

        try:
            client.utility.verify_payment_signature(request.POST)

            print("payment success")

            order_id=request.POST.get("razorpay_order_id")


            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)

            

            

            cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

            for ci in cart_items:
                ci.is_order_placed=True

                ci.save()

        except:
            print("payment failed")

        
        return redirect("home")
    

class MyOrdersView(View):
    def get(self,request,*args,**kwargs):

        cartitems=OrderSummary.objects.filter(user_object=request.user,is_paid=True)

        return render(request,"my_orders.html",{"orders":cartitems})
 


class SearchView(ListView):
    model = Project
    template_name = 'result.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            product = Project.objects.filter(title__contains=query)
            result = product
        else:
            result = None

        return result