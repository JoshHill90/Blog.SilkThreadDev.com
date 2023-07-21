from django.contrib import admin
from.models import Blog, Category, MetaTags, Comments
 
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(MetaTags)
@admin.register(Comments)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('email', 'comment', 'blog', 'time_stamp', 'active')
    list_filter = ('active', 'time_stamp')
    search_fields = ('user', 'post')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)