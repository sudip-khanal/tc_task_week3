from django.contrib import admin
from apps.book.models import Book,Favorite
"""
Register models in django admin using ModelAdmin which Encapsulate
all admin options and functionality for a given model.
"""
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','author', 'created_by', 'description','is_active','created_at','updated_at')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id','user','book')

admin.site.register( Book,BookAdmin)
admin.site.register( Favorite,FavoriteAdmin)

