from django.urls import path
from .views import *
from . import views

urlpatterns = [
        path('', IndexView.as_view(), name='index'),
        path('contact/', ContactView.as_view(), name='contact'),
        path('about/', about_page, name='about'),
        path('blog/', views.all_blogs, name='blogs'),
        path('blog/<int:pk>/', views.blog_details, name='blog-details'),
        path('blog/<int:pk>/edit', BlogEditView.as_view(), name='blog-edit'),
        path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name='blog-delete'),
        path('blog/create', BlogCreateView.as_view(), name='blog-create'),
        path('category/', CategoryCreateView.as_view(), name='category'),
        path('meta-tags/', MetaTagCreateView.as_view(), name='meta-tags'),
        path('success/', success, name='success'),
]