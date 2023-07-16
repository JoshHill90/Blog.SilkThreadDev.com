from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .models import Blog, Category, MetaTags, Contact, Comments
from .forms import BlogForm, CategoryForm, ContactForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from blog_project.env.injector import SETTINGS_KEYS as sk



#-------------------------------------------------------------------------------------------------------#
# blog views
#-------------------------------------------------------------------------------------------------------#

def blog_details(request, id):
    template_name = 'blog/blog-details.html'
    blog = get_object_or_404(Blog, pk=id)
    comments = blog.comments.filter(active=True)
    new_comments = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()

        return render(request, template_name, {
            'blog': blog,
            'comments': comments,
            'new_comments': new_comments,
            'comment_form': comment_form
        })


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog-create.html'

class BlogEditView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog-edit.html'

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog-delete.html'
    success_url = reverse_lazy('success')

def all_blogs(request):
    all_category = Blog.objects.all()
    category_list = Category.objects.all()
    tags_list = MetaTags.objects.all()
    return render(request, 'bloh/blogs.html', {
        'all_category': all_category,
        'category_list': category_list,
        'tags_list': tags_list
        }
    )
#-------------------------------------------------------------------------------------------------------#
# meta_tags views
#-------------------------------------------------------------------------------------------------------#

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'meta_tags/create-category.html'
    success_url = reverse_lazy('success-category')

class MetaTagCreateView(CreateView):
    model = MetaTags
    fields = '__all__'
    template_name = 'meta_tags/create-category.html'
    success_url = reverse_lazy('success-meta')

#-------------------------------------------------------------------------------------------------------#
# models class
#-------------------------------------------------------------------------------------------------------#


class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    ordering =['-id']


class ContactView(FormView):
    model = Contact
    template_name = 'meta_tags/contact.html'
    
    def form_valid(self, form):
        self.object = form.save()
        name = self.object.name
        email = self.object.email
        subject = self.object.subject
        body = self.object.body

        send_mail(
            subject,
            f'From {name}, Subject: {body}',
            email, 
            [sk.emun]
        )
        context = {
            'type': 'contact',
            'name': name,
            'email': email,
            'subject': subject
        }
        return redirect('success', context)
    
def about_page():
    return render('about.html')

def success(context):
    #validate context type for success massage

    return render('success.html', context)

