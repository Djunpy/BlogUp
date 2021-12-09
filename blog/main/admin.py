from django.contrib import admin


from .models import Post, Tag, Category
from .forms import PostAdminForm


@admin.register(Post)
class PostPanel(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'created', 'status', 'category')
    list_filter = ('title', 'status', 'category', 'publish', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status',)
    date_hierarchy = 'publish'
    ordering = ('publish', 'status')


@admin.register(Category)
class CategoryPanel(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagPanel(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
