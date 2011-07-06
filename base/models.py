import datetime
import os
import random
import shutil
import zipfile

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse, reverse
from django.db import models
from django.db.models import permalink
from django_extensions.db.fields import AutoSlugField
from imagekit.models import ImageModel, CROP_HORZ_CHOICES, CROP_VERT_CHOICES
from sjutils.models import SelfAwareModel
from sjutils import EXIF 
from sjphoto.base.managers import GalleryManager, FeaturedManager
from likeables.models import Likeable

#from photologue.models import Gallery, Photo

class Photo( ImageModel, SelfAwareModel ):
    title      = models.CharField(max_length=100, unique=True, 
                                  db_index=True, blank=False, null=False )
    image = models.ImageField('image', max_length=255, 
                              upload_to='photos/')
    date_taken = models.DateTimeField('date taken', null=True, blank=True, editable=False)
   
    slug       = AutoSlugField( populate_from=('title',) )
    caption    = models.CharField(max_length=255, blank=True, null=True)
    crop_from_vertical = models.SmallIntegerField("Crop From",choices=CROP_VERT_CHOICES, default=1)
    crop_from_horizontal = models.SmallIntegerField("Crop From", choices=CROP_HORZ_CHOICES, default=1)
    is_public  = models.BooleanField('is public', default=True, help_text='Public photographs will be displayed in the default views.')
    likes      = generic.GenericRelation( Likeable )
    
    class IKOptions:
        spec_module = 'base.specs'
        cache_dir = 'photos'
        image_field = 'image'
        crop_horz_field = 'crop_from_horizontal' 
        crop_very_field = 'crop_from_vertical'
        
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return u'%s' % self.title
    @property
    def EXIF(self):
        try:
            return EXIF.process_file(open(self.image.path, 'rb'))
        except:
            try:
                return EXIF.process_file(open(self.image.path, 'rb'), details=False)
            except:
                return {}
            
    def save(self, *args, **kwargs):
        if self.date_taken is None:
            try:
                exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = str.split(exif_date.values)
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    self.date_taken = datetime(int(year), int(month), int(day),
                                               int(hour), int(minute), int(second))
            except:
                pass
        if self.date_taken is None:
            self.date_taken = datetime.datetime.now()
        if self._get_pk_val():
            self.clear_cache()
        super(ImageModel, self).save(*args, **kwargs)
    def get_created( self ):
        return self.created.strftime("%B %d, %Y")
    

    get_created.short_description = 'Date Created'
    
class Gallery( SelfAwareModel ):
    title       = models.CharField(max_length = 80, blank=False, null=False)
    slug        = AutoSlugField( populate_from=('title',) )
    photos      = models.ManyToManyField( 'Photo', verbose_name="Photos", related_name="galleries" )
    description = models.TextField('Description', blank=True, help_text='A description of this Gallery.')
    is_public   = models.BooleanField('is public', default=True, help_text='Public photographs will be displayed in the default views.')
    feature     = models.BooleanField('Featured', default=False, help_text='Featured Galleries will be displayed On the home page')
    admin_objects = models.Manager()
    objects     = GalleryManager()
    featured    = FeaturedManager()
    likes      = generic.GenericRelation( Likeable )
    class Meta:
        verbose_name_plural = "Galleries"
        get_latest_by  = 'created'
        
    def photo_count(self):
        return self.photo.all().count()

    def __unicode__(self):
        return u'%s' % self.title
         
class GalleryUpload(models.Model):
    zip_file    = models.FileField('images file (.zip)', upload_to="photos/temp",
                                help_text='Select a .zip file of images to upload into a new Gallery.')
    gallery     = models.ForeignKey(Gallery, null=True, blank=True, help_text='Select a gallery to add these images to. leave this empty to create a new gallery from the supplied title.')
    title       = models.CharField('title', max_length=75, help_text='All photos in the gallery will be given a title made up of the gallery title + a sequential number.')
    caption     = models.TextField('caption', blank=True, help_text='Caption will be added to all photos.')
    description = models.TextField('description', blank=True, help_text='A description of this Gallery.')
    is_public   = models.BooleanField('is public', default=True, help_text='Uncheck this to make the uploaded gallery and included photographs private.')

    class Meta:
        verbose_name = 'gallery upload'
        verbose_name_plural = 'gallery uploads'

    def save(self, *args, **kwargs):
        super(GalleryUpload, self).save(*args, **kwargs)
        gallery = self.process_zipfile()
        super(GalleryUpload, self).delete()
        return gallery

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            if self.gallery:
                gallery = self.gallery
            else:
                gallery = Gallery.objects.create(title=self.title,
                                                 title_slug=slugify(self.title),
                                                 description=self.description,
                                                 is_public=self.is_public,
                                                 tags=self.tags)
            from cStringIO import StringIO
            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = Image.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = Image.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    while 1:
                        title = ' '.join([self.title, str(count)])
                        slug = slugify(title)
                        try:
                            p = Photo.objects.get(title_slug=slug)
                        except Photo.DoesNotExist:
                            photo = Photo(title=title,
                                          title_slug=slug,
                                          caption=self.caption,
                                          is_public=self.is_public,)
                            photo.image.save(filename, ContentFile(data))
                            gallery.photos.add(photo)
                            count = count + 1
                            break
                        count = count + 1
            zip.close()
            return gallery

class PhotoContest(SelfAwareModel):
    title   =  models.CharField(max_length=255, blank=False, null=False)
    slug    =  models. SlugField()
    end_date = models.DateTimeField(blank=False, null=False)
    photos =   models.ManyToManyField(Photo)
    voters =   models.ManyToManyField(User, editable=False, null=True, blank=True)
    class Meta:
        pass
    
    def __unicode__(self):
        return self.title
    @permalink
    def get_absolute_url(self):
        return ('sjphoto.base.views.contests.photo_contest_detail',(),{
                       'slug':self.slug,
                       'ct_id':self.get_ct_id(),
                       'obj_id':self.id
               })
    def is_closed(self):
        n = datetime.datetime.now()
        result ( n > self.end_date )
        return result
