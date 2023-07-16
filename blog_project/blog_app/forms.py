from django import forms
from .models import Blog, Category, Contact, Comments

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'author', 'artical', 'preview', 'category', 'image_url')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'artical': forms.Textarea(attrs={'class': 'form-control'}),
            'preview' : forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ('name', 'meta_tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'meta_tags': forms.Select(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message Body'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('user', 'post')
