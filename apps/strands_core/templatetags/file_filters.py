from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

import os

@register.filter
@stringfilter
def filename(value):
    # returns just the filename itself
    # for file.name = '../uploads/foo.ext', {{ bar.file.name|filename }} yields 'foo.ext'
    return os.path.split(value)[1]

@register.filter
def pretty_size(bytes, precision=1):
    # returns a filesize in human-friendly units
    # based on snippet from http://code.activestate.com/recipes/577081-humanized-representation-of-a-number-of-bytes/
    #
    # arg is an integer describing the decimal precision of the displayed size
    # for file.size = 7250, {{ bar.file.size|pretty_size:0 }} yields '7 KiB'
    units = (
        (1<<50L, 'PiB'),
        (1<<40L, 'TiB'),
        (1<<30L, 'GiB'),
        (1<<20L, 'MiB'),
        (1<<10L, 'KiB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in units:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)