DEBUG = False

DEFAULT_STORAGE = 'synclee.easy_thumbnails.storage.ThumbnailFileSystemStorage'
MEDIA_ROOT = ''
MEDIA_URL = ''

BASEDIR = ''
SUBDIR = ''
PREFIX = ''

QUALITY = 85
EXTENSION = 'jpg'
TRANSPARENCY_EXTENSION = 'png'
PROCESSORS = (
    'synclee.easy_thumbnails.processors.colorspace',
    'synclee.easy_thumbnails.processors.autocrop',
    'synclee.easy_thumbnails.processors.scale_and_crop',
    'synclee.easy_thumbnails.processors.filters',
)
SOURCE_GENERATORS = (
    'synclee.easy_thumbnails.source_generators.pil_image',
)
