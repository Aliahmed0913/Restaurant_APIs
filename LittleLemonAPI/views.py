from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from django.contrib.auth.models import User,Group
from rest_framework.response import Response
from . import serializers ,models , permissions
from rest_framework import viewsets,status,throttling
from django.utils.timezone import now


@api_view(['POST','GET','DELETE'])
@permission_classes([permissions.isManager])
@throttle_classes([throttling.UserRateThrottle])
def managers_activate(request,pk=0):
   
    manager = Group.objects.get(name='Manager')
    A_username = request.data.get('username')
    managers = User.objects.all().filter(groups__name='Manager').values('id','username')
   
    if request.method == 'POST':
        user = get_object_or_404(User,username=A_username)
        manager.user_set.add(user)
        return Response(f'user : {A_username} => became a manager',201)
   
    elif request.method == 'GET':
        return Response({'Managers':managers})
    
    elif request.method == 'DELETE':
        R_username = User.objects.get(id=pk)
        if R_username.groups.filter(name='Manager').exists():
            manager.user_set.remove(R_username)
            return Response(managers,200)
        return Response(status=404)
    
@api_view(['GET','POST','DELETE'])
@permission_classes([permissions.isManager])
@throttle_classes([throttling.UserRateThrottle])
def Delivery_Crew_func(request,pk=0):
   
    A_username = request.data.get('username')
    Delivery_crew = Group.objects.get(name='delivery_crew')
    delivery_crews = User.objects.all().filter(groups__name='delivery_crew').values('id','username')
    
    if request.method == 'GET':
        return Response({'delivery_crews':delivery_crews})
    
    if request.method == 'POST':
        user = get_object_or_404(User,username=A_username)
        Delivery_crew.user_set.add(user)
        return Response(f'user : {A_username} => belon to Delivery_crew',201)
    
    elif request.method == 'DELETE':
        R_username = User.objects.get(id=pk)
        if R_username.groups.filter(name='Manager').exists():
            Delivery_crew.user_set.remove(R_username)
            return Response(delivery_crews,200)
        return Response(status=404)
        
        
class MenuItemsView(viewsets.ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    throttle_classes=[throttling.UserRateThrottle]
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            self.permission_classes = [permissions.isManager]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    


@api_view()
def menuitem_detail(request,pk):
    menuitem = get_object_or_404(models.MenuItem,pk=pk)
    serialized_item = serializers.MenuItemSerializer(menuitem)
    return Response(serialized_item.data)

class WorkWithCart(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer
    queryset=models.Cart.objects.all()
    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user)

    def destroy(self,requst):
        user = User.objects.get(username=requst.user)
        user_cart = models.Cart.objects.filter(user=user)
        if user_cart:
            user_cart.delete()
            return Response('Cart is free!',status=200)
        return Response('No items!',400)
    
class OrderItemsView(viewsets.ModelViewSet):
    queryset = models.Orderitem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    throttle_classes = [throttling.UserRateThrottle]
    def update(self, request,pk):
        order_data = models.Order.objects.filter(id=pk)
       
        if order_data:
          order_status = self.request.data.get('status')
          delivery_crew = self.request.data.get('delivery_crew')
          
          if delivery_crew:
              username = User.objects.get(username=delivery_crew)
             
          if self.request.user.groups.filter(name='Manager').exists(): 
            
              if username.groups.filter(name='delivery_crew').exists():
                  updated_data={'delivery_crew':username,'status':order_status}
                  order_data.update(**updated_data)
                  serialized_order = serializers.OrderSerializer(order_data,many=True)
                
                  return Response(serialized_order.data)
             
              return Response(f'{username.username.capitalize()} isn\'t an delivery person ',status=status.HTTP_400_BAD_REQUEST)
         
          elif self.request.user.groups.filter(name='delivery_crew').exists():
              updated_data = {'status':order_status}
              order_data.update(**updated_data)
              serialized_order = serializers.OrderSerializer(order_data,many=True)
              return Response(serialized_order.data)
       
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_queryset(self):
       
        if self.request.user.groups.filter(name='Manager').exists():
            return models.Orderitem.objects.all()
        if self.request.user.groups.filter(name='delivery_crew').exists():
            return models.Orderitem.objects.filter(order__delivery_crew=self.request.user)
            
       
        return models.Orderitem.objects.filter(order__user=self.request.user) 
    def retrieve(self, request,pk):
        items = models.Orderitem.objects.filter(order__user=self.request.user,order_id=pk)
        if not items.exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        serialized_orederitem = serializers.OrderItemSerializer(items,many=True)
        return Response(serialized_orederitem.data) 
    def create(self,request):
        user = request.user
        cart_items = models.Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response('Error! . this cart isnot exist',status=status.HTTP_400_BAD_REQUEST)
        
        total = sum(item.unit_price*item.quantity for item in cart_items)
        order = models.Order.objects.create(user=user,total=total,date=now().date())
        
        order_items = []
        for item in cart_items:
            order_items.append(models.Orderitem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.unit_price*item.quantity
            ))
        models.Orderitem.objects.bulk_create(order_items)
        cart_items.delete()
        return Response('order created succes',status=status.HTTP_201_CREATED)



