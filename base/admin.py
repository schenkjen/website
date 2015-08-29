from django.contrib import admin
from sjphoto.base.models import PhotoContest, Photo, Gallery
from django.core import management


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail_view','title', 'is_public', 'get_created' )
    list_filter  = ('created', 'is_public' )
    list_display_links = ('title',)
    date_hierarchy = 'created'
    actions = ['flush_thumbnails']
    
    def flush_thumbnails(self, request, queryset):
        management.call_command('ikflush', 'base')
        self.message_user( request, "Images Successfully Updated")
    flush_thumbnails.short_description = "Update Images and Thumbnails"

    

class GalleryAdmin( admin.ModelAdmin ):
    list_display = ('title', 'created', 'photo_count')
    list_filter = ['created', 'is_public']
    date_hierarchy = 'created'
    filter_horizontal = ("photos", )
    
class ClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('photos',)
    
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoContest)
