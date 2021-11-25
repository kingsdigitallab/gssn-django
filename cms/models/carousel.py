

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from .links import AbstractLinkFields


class AbstractCarouselItem(AbstractLinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    caption = models.CharField(max_length=38, blank=True)
    description = RichTextField(blank=True)
    copyright = RichTextField(blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        MultiFieldPanel(AbstractLinkFields.panels, 'Link'),
        FieldPanel('description'),
        FieldPanel('copyright'),
    ]

    class Meta:
        abstract = True
