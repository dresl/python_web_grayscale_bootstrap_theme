from blog.models import Blog
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    list_filter = ('title'),
    search_fields = ('title'),
    list_display = ('title', 'pub_date')
    fieldsets = [
        ('Title',               {'fields': ['title']}),
        ('Date information', {'fields': ['pub_date']}), #'classes': ['collapse']
        ('Content',               {'fields': ['body']}),
        ('Thumbnail',            {'fields': ['thumbnail']}),
        ('Likes',            {'fields': ['users_like_it']}),
    ]
    filter_horizontal = ('users_like_it',)

admin.site.register(Blog, BlogAdmin)
