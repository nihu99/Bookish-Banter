from django.contrib import admin
from .models import *

class AdminProduct(admin.ModelAdmin):
    list_display = ['productTitle','productPrice','productCategory']

class AdminCategory(admin.ModelAdmin):
    list_display = ['categoryName']

# Register your models here.
class PostCreated(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(order)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(blog, PostCreated) 
admin.site.register(BookingForm)
admin.site.register(FeaturedProduct)
admin.site.register(News)
admin.site.register(NewsCategory)
admin.site.register(Partners)
admin.site.register(Donate)
admin.site.register(Contact)
admin.site.register(Statistic)