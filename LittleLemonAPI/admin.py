from django.contrib import admin
from . import models as m
# Register your models here.
admin.site.register(m.Category)
admin.site.register(m.MenuItem)
admin.site.register(m.Cart)
admin.site.register(m.Order)
admin.site.register(m.Orderitem)