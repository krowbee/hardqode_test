from django.contrib import admin

from lessons.models import Product, Viewing,Lesson

# Register your models here.

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Viewing)