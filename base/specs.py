from imagekit import processors
from imagekit.specs import ImageSpec

# Processors

class Enhance( processors.Adjustment ):
    contrast  = 1.3
    sharpness = 1.4
    
class DisplayResize(processors.Resize):
    height = 1000
    width  = 1000
    crop   = False
    

class FeatureResize( processors.Resize ):
    height    = 530
    width     = 800
    crop      = True


class FeatureThumbResize( processors.Resize ):
    height = 40
    width  = 40
    crop   = True 
    
    

class GalleryResize( processors.Resize ):
    width = 600


class PreviewResize( processors.Resize ):
    height  = 220
    width   = 340
    crop    = True
    upscale = True


class BlogResize( processors.Resize ):
    width  = 250
    height = 250
    

class BlogManagerResize( processors.Resize ):
    height = 140
    width  = 140
    crop   = True


class ThumbnailResize( processors.Resize ):
    height = 60
    width  = 60

class AdminThumbnailResize( processors.Resize ):
    height = 80
    width  = 80
    cropt  = True
class BlogThumbResize ( processors.Resize ):
    height = 40
    width  = 40
    crop   = True
    

class SearchResize( processors.Resize ):
    height = 45
    width  = 45
    crop   = True




# Define Image Specs
class Display( ImageSpec ):
    processors = [ DisplayResize ]
    pre_cache  = True
    quality    = 80
    
class Feature( ImageSpec ):
    processors = [ FeatureResize ]
    pre_cache = True
    quality   = 90
    
class Gallery( ImageSpec ):
    processors = [ GalleryResize ]
    pre_cache = True
    
class GalleryPreview( ImageSpec ):
    processors = [ PreviewResize ]
    pre_cache = True
    access_as = 'gallery_preview'
    
class Blog( ImageSpec ):
    processors = [ BlogResize ]
    pre_cache = True
    
class BlogManage( ImageSpec ):
    processors = [ BlogManagerResize ]
    pre_cache = False
    
class Thumbnail( ImageSpec ):
    processors = [ ThumbnailResize ]
    quality = 60
class admin_thumbnail( ImageSpec ):
    processors = [AdminThumbnailResize]
    quality = 60
class BlogThumb( ImageSpec ):
    processors = [ BlogThumbResize ]
    quality = 50
    
class Search( ImageSpec ):
    processors = [ SearchResize ]
    quality    = 50
    pre_cache  = True

class FeatureThumb( ImageSpec ):
    processors = [ FeatureThumbResize, Enhance ]
    pre_cache  = True
    quality    = 50
    access_as  = 'feature_thm'