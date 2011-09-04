from djapian import space, Indexer
from sjphoto.base.models import Gallery

class GalleryIndexer(Indexer):
    fields = ['title', 'description']
    tags = [
        ('title', 'title', 3),
        ('description', 'description', 2)
    ]

space.add_index(Gallery, GalleryIndexer, attach_as="indexer")