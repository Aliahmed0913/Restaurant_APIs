from django.urls import path
from . import views

urlpatterns=[
    path('groups/manager/users',views.managers_activate),
    path('groups/manager/users/<int:pk>',views.managers_activate),
    
    path('groups/delivery-crew/users',views.Delivery_Crew_func),
    path('groups/delivery-crew/users/<int:pk>',views.Delivery_Crew_func),
    
    path('menu-items',views.MenuItemsView.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>',views.MenuItemsView.as_view({'get':'retrieve' ,'post':'create'
        ,'put':'update'
        ,'delete':'destroy'
        ,'patch':'partial_update'})),
    
    path('cart/menu-items',views.WorkWithCart.as_view({'get':'list','post':'create','delete':'destroy'})),
    path('cart/menu-items/<int:pk>',views.menuitem_detail , name='menuitem_detail'),
    
    
    path('orders',views.OrderItemsView.as_view({'get':'list','post':'create'}) , name='menuitem_detail'),
    path('orders/<int:pk>',views.OrderItemsView.as_view({'get':'retrieve','put':'update','delete':'destroy'}) , name='menuitem_detail')
]