from __future__ import unicode_literals

from django import forms

from wagtail.wagtailcore.blocks import (
    CharBlock, FieldBlock, PageChooserBlock, RawHTMLBlock, RichTextBlock,
    StreamBlock, StructBlock, TextBlock, URLBlock
)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = 'code'


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'),
        ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class EmailBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.EmailField(help_text=help_text, required=required)
        super(EmailBlock, self).__init__(**kwargs)


class LinkBlock(StructBlock):
    page = PageChooserBlock(icon='wagtail', required=False)
    url = URLBlock(icon='link', required=False)
    document = DocumentChooserBlock(icon='doc-full-inverse', required=False)
    email = EmailBlock(icon='mail', required=False)
    label = CharBlock(max_length=32)

    class Meta:
        icon = 'link'


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


class CMSStreamBlock(StreamBlock):
    h2 = CharBlock(classname='title', icon='title')
    h3 = CharBlock(classname='title', icon='title')
    h4 = CharBlock(classname='title', icon='title')
    h5 = CharBlock(classname='title', icon='title')
    intro = RichTextBlock(icon='pilcrow')
    paragraph = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock()

    image = ImageBlock(icon='image', label='Aligned image')
    link = LinkBlock()

    embed = EmbedBlock(icon='media')

    html = AlignedHTMLBlock(label='Raw HTML')
    map_html = AlignedHTMLBlock(label='Map HTML')
