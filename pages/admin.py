from django.contrib import admin
from .models import Movie
from django.shortcuts import render


# config file for built in django admin app
# Register your models here.


# class PostAdmin(admin.ModelAdmin):
#     def save_model(self, obj, request, form, change):
#         if not change:
#             obj.created_by = request.user
#         obj.save()


admin.site.register(Movie)
# admin.site.register(Movie, PostAdmin)
