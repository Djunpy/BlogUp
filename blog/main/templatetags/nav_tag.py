from django import template
from ..models import Category, Post, Tag


register = template.Library()


@register.inclusion_tag('main/inc/nav_menu.html')
def show_category():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('main/inc/show_tags.html')
def show_tags(cnt=10):
    tags = Tag.objects.all()[:cnt]
    return {'tags': tags}


@register.inclusion_tag('main/popular_posts.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}
