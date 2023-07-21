from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Blog, Category, MetaTags, Contact, Comments
from .forms import BlogForm, CategoryForm, ContactForm, CommentForm
from django.core.mail import send_mail

from blog_project.env.injector import SETTINGS_KEYS as sk



#-------------------------------------------------------------------------------------------------------#
# blog views
#-------------------------------------------------------------------------------------------------------#

def blog_details(request, pk):
    template_name = 'blog/blog-details.html'
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.filter(active=True)
    new_comments = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.save()
            return render(request, 'blog/comment_success.html', {
                'name': comment_form.cleaned_data.get('name'),
                'email': comment_form.cleaned_data.get('email'),
                'comment': comment_form.cleaned_data.get('comment'),
                'blog': blog
            })

    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'blog': blog,
        'comments': comments,
        'new_comments': new_comments,
        'comment_form': comment_form
    })
    
class CommentSuccessView(TemplateView):
    template_name = 'blog/comment_success.html'

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
    success_url = reverse_lazy('index')

def all_blogs(request):
    blog_list = Blog.objects.all()
    category_list = Category.objects.all()
    tags_list = MetaTags.objects.all()

    title_query = request.GET.get('title')
    keyword_query = request.GET.get('keyword')
    category_query = request.GET.get('category')
    tag_query = request.GET.get('tag')

    if category_query == 'Category' and  category_query is not None:
        blog_list = Blog.objects.all()
    else:
        blog_list = Blog.objects.filter(category__exact=category_query)

    if tag_query == 'Tags' and tag_query is not None:
        blog_list = Blog.objects.all()
    else:
        try:
            tag_obj = MetaTags.objects.get(tags__iexact=tag_query)
            categories_with_tag = Category.objects.filter(meta_tags=tag_obj)
            blog_list = blog_list.filter(category__in=categories_with_tag)
        except MetaTags.DoesNotExist:
            blog_list = Blog.objects.none()


    if title_query != '' and  title_query is not None:
        blog_list = Blog.objects.filter(title__icontains=title_query)
    
    if keyword_query != '' and  keyword_query is not None:
        blog_list = Blog.objects.filter(
            Q(title__icontains=keyword_query) | Q(artical__icontains=keyword_query)
            )
    if title_query != '' and  title_query is not None and keyword_query != '' and  keyword_query is not None and category_query == 'Category' and  category_query is not None and tag_query == 'Tags' and tag_query is not None:
        blog_list = Blog.objects.all()
        
    return render(request, 'blog/blogs.html', {
        'blog_list': blog_list,
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
    success_url = reverse_lazy('category')


#-------------------------------------------------------------------------------------------------------#
# models class
#-------------------------------------------------------------------------------------------------------#


class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    ordering =['-id']


class ContactView(FormView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm
    
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
        return redirect('contact-success', context)
    
class ContactSuccessView(TemplateView):
    template_name = 'contact-success.html'
    
def about_page():
    return render('about.html')


