from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Blog, Category, MetaTags, Contact, Comments
from .forms import BlogForm, ContactForm, CommentForm
from blog_project.env.MailerDJ import AutoReply

EMAIL = AutoReply()

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
                'user_id': comment_form.cleaned_data.get('user_id'),
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
    orrder_query = request.GET.get('order')
    
    
    if not (keyword_query or title_query or category_query == "Category" or tag_query =="Tags"):
        blog_list = Blog.objects.all()
    elif keyword_query:
        blog_list = Blog.objects.filter(
            Q(title__icontains=keyword_query) | Q(article__icontains=keyword_query)
            )
    elif title_query:
        blog_list = Blog.objects.filter(title__icontains=title_query)
    elif category_query != 'Category':
        blog_list = Blog.objects.filter(category__exact=category_query)
    elif tag_query != 'Tags':
        try:
            tag_obj = MetaTags.objects.get(tags__iexact=tag_query)
            categories_with_tag = Category.objects.filter(meta_tags=tag_obj)
            blog_list = blog_list.filter(category__in=categories_with_tag)
        except MetaTags.DoesNotExist:
            blog_list = Blog.objects.all()
    elif keyword_query == None and title_query == None and category_query == "Category" and tag_query == "Tags":
        blog_list = Blog.objects.all()
    
    if orrder_query == 'Oldest':
        blog_list = blog_list.order_by('time_stamp')
    else:
        blog_list = blog_list.order_by('-time_stamp')
        
    
    return render(request, 'blog/blogs.html', {
        'blog_list': blog_list,
        'category_list': category_list,
        'tags_list': tags_list
        }
    )
#-------------------------------------------------------------------------------------------------------#
# meta_tags views
#-------------------------------------------------------------------------------------------------------#

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

        EMAIL.contact_request(email, name)
        EMAIL.contact_alart(email, name, subject, body)

        return redirect('contact-success')
    
class ContactSuccessView(TemplateView):
    template_name = 'contact-success.html'
    


