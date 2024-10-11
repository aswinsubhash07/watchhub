from django.db import models

from django.contrib.auth.models import User

from django.db.models import Sum

class UserProfile(models.Model):

    bio=models.CharField(max_length=260)

    profile_pic=models.ImageField(upload_to="profile_picture",default="/profile_picture/defaulf.png")

    user_object=models.OneToOneField(User, on_delete=models.CASCADE)

    created_date=models.DateTimeField(auto_now=True)

    updated_date=models.DateTimeField(auto_now_add=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user_object.username

    


class Tag(models.Model):

    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    



class Project(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    tag_objects=models.ManyToManyField(Tag)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")

    watch_pic=models.ImageField(upload_to="watch_picture",default="/watch_picture/default_png")

    weight=models.CharField(max_length=200)

    case=models.CharField(max_length=200)

    band=models.CharField(max_length=200)

    water_resistance=models.CharField(max_length=200)

    country_orgin=models.CharField(max_length=200)

    color=models.CharField(max_length=200)

    price=models.PositiveIntegerField()
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.title




class WishList(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def wishlist_total(self):

        return self.basket_items.filter(is_order_placed=False).values("project_object__price").aggregate(total=Sum('project_object__price')).get("total")


# request.user.basket.basket_items.all()
class WishListItems(models.Model):

    wishlist_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="basket_items")

    project_object=models.ForeignKey(Project,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    

class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    project_objects=models.ManyToManyField(Project)

    order_id=models.CharField(max_length=200,null=True)

    name=models.CharField(max_length=200)

    address=models.CharField(max_length=200)

    phone=models.CharField(max_length=200)

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField()


from django.db.models.signals import post_save

def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)




post_save.connect(sender=User,receiver=create_profile)



def create_basket(sender,instance,created,*args,**kwargs):

    if created:

        WishList.objects.create(
          owner=instance  
        )


post_save.connect(sender=User,receiver=create_basket)