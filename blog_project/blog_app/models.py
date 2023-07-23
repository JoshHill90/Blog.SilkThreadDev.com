from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from ckeditor.fields import RichTextField

#-------------------------------------------------------------------------------------------------------#
# models class
#-------------------------------------------------------------------------------------------------------#

class MetaTags(models.Model):
    tags = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.tags)
    
    def get_absolute_url(self):
        return reverse("meta-tag")
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    meta_tags = models.ManyToManyField(MetaTags,blank=True)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("category", args=(str(self.name)))
    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = RichTextField(blank=True, null=True)
    preview = models.CharField(max_length=255, blank=True)
    time_stamp = models.DateField(auto_now=True)
    image_url = models.URLField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null='True')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.title + ' by ' + self.author.first_name + ' ' + self.author.last_name)

    def get_absolute_url(self):
        return reverse("blog-details", args=(str(self.id)))


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField(max_length=800)

    def __str__(self):
        return f'Name: {self.name} - Subject: {self.subject}'
    
    def get_absolute_url(self):
        return reverse("contact-success")
    
class Comments(models.Model):
    email = models.EmailField(max_length=255, default='none@none.com')
    name = models.CharField(max_length=50, default='none')
    comment = models.TextField(max_length=500)
    time_stamp = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    
    
    class Meta:
        ordering = ['time_stamp']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.email)
    

    

    