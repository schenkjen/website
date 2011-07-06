from django import template
from django.template import Library, Node, TemplateSyntaxError
import pdb
register = Library()

class ExifForPropertyForPhoto(Node):
    def __init__(self, photo, exif_key):
        self.photo = template.Variable(photo)
        self.key = exif_key
    def __repr__(self):
        return "<exif node>"

    def render(self, context):
        the_photo = self.photo.resolve(context)
        the_key = ' '.join(self.key.split('_'))
        #pdb.set_trace()
        try:
            data = "%s" % the_photo.EXIF[the_key]
        except KeyError:
            data = "unknown"


        return data

def doExifForPropertyForPhoto(parser, token):
    '''{% exif  %}'''
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "exif tag takes exactly 2 arguments"
    else:
        return ExifForPropertyForPhoto(bits[1], bits[2])

register.tag('exif', doExifForPropertyForPhoto)
