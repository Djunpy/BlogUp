from .models import Post, Category, Tag, Comment, Contact
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F
from .forms import CommentForm, ContactForm
from allauth.account.views import SignupView, LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail


Login = LoginView
Signup = SignupView
Logout = LogoutView


class IndexPage(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.filter(status='published')
    template_name = 'main/index.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class SinglePage(DetailView):
    model = Post
    template_name = 'main/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(SinglePage, self).get_context_data(**kwargs)

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']

        post = get_object_or_404(Post, slug=slug, pk=pk)

        context['form'] = CommentForm
        context['post'] = post
        return context

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        self.object = self.get_object(**kwargs)
        comments = post.comments.filter(active=True)

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            body = form.cleaned_data['body']

            comment = Comment.objects.create(name=name, email=email,
                                             body=body, post=post)
            form = CommentForm()
            context['form'] = form

            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class ByCategory(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/index.html'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ByCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], status='published')


class ByTag(ListView):
    allow_empty = False
    context_object_name = 'posts'
    template_name = 'main/index.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ByTag, self).get_context_data(**kwargs)
        context['title'] = 'Записи по тегу' + ' ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])


class Search(ListView):
    template_name = 'main/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['s'] = f'{self.request.GET.get("s")}&'
        return context

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))



