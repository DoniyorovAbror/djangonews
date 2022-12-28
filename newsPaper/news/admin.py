from django.contrib import admin
from .models import Post, Category, Author
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "preview",)
    list_filter = ("dateCreation",)
    search_fields = ('title', 'text', 'postCategory__category_name',)
    fields = ('title', 'text', 'author', 'categoryType')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
