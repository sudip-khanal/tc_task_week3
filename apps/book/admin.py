from django.contrib import admin
from apps.book.models import Book,Favorite

class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'created_by', 'description','is_active','created_at','updated_at')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user','book')

admin.site.register( Book,BookAdmin)
admin.site.register( Favorite,FavoriteAdmin)

