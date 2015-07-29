from django.contrib import admin
from userprofile.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',               {'fields': ['user']}),
        ('Profile picture', {'fields': ['profile_picture']}),
        ('Hobbies', {'fields': ['hobbies']}),
    ]

admin.site.register(UserProfile, UserProfileAdmin)