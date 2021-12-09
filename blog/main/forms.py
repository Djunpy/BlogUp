from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment, Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']