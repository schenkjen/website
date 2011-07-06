from django.db.models import Manager

class GalleryManager( Manager ):
    
    def get_query_set(self):
        return super(GalleryManager, self).get_query_set().filter( is_public = True )

class FeaturedManager( Manager ):
    def get_query_set(self):
        return super(FeaturedManager, self).get_query_set().filter( feature = True)