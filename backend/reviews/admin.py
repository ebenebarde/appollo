from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('track', 'user', 'rating', 'created_at')
    search_fields = ('track__title', 'track__album__title', 'track__album__artist__name', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)