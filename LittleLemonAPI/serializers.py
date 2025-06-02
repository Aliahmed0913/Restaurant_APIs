from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['id','title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all()
    )
    class Meta:
        model = models.MenuItem
        fields = ['id','title','price','category','featured']
        
        
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=models.MenuItem.objects.all()
    )
    price = serializers.SerializerMethodField(method_name='total_price',default=0)
    class Meta:
        model = models.Cart
        fields = ['user','menuitem','quantity','unit_price','price']

    def total_price(self,item:models.Cart):
        return item.unit_price * item.quantity
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'user', 'delivery_crew', 'status','total','date']
        
class OrderItemSerializer(serializers.ModelSerializer):

    order_id= serializers.IntegerField()

    class Meta:
        model = models.Orderitem
        fields = ['order_id','menuitem','quantity','unit_price','price']
