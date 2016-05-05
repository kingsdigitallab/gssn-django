from __future__ import unicode_literals

from datetime import date
import logging

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel,
    StreamFieldPanel
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from .behaviours import WithFeedImage, WithIntroduction, WithStreamField
from .carousel import AbstractCarouselItem
from .links import AbstractRelatedLink
from .streamfield import CMSStreamBlock

logger = logging.getLogger(__name__)


# HomePage
class HomePageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


class HomePageFeaturedPage(Orderable):
    page = ParentalKey('HomePage', related_name='featured_pages')
    featured_page = models.ForeignKey(Page)

    panels = [
        PageChooserPanel('featured_page')
    ]

    def __unicode__(self):
        return self.featured_page


class HomePageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')


class HomePage(Page, WithStreamField):
    announcement = StreamField(CMSStreamBlock())

    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('announcement'),
    )

    subpage_types = ['IndexPage', 'BlogIndexPage', 'EventIndexPage',
                     'SymposiumIndexPage', 'RichTextPage']

    class Meta:
        verbose_name = 'Homepage'

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
    InlinePanel('featured_pages', label='Featured pages'),
    InlinePanel('carousel_items', label='Carousel items'),
    StreamFieldPanel('announcement'),
    InlinePanel('related_links', label='Related links'),
]

HomePage.promote_panels = Page.promote_panels


# IndexPage
class IndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('IndexPage', related_name='related_links')


class IndexPage(Page, WithFeedImage, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['IndexPage', 'RichTextPage']

IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('intro'),
    InlinePanel('related_links', label='Related links'),
]

IndexPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


# RichTextPage
class RichTextPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('RichTextPage', related_name='carousel_items')


class RichTextPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('RichTextPage', related_name='related_links')


class RichTextPage(Page, WithFeedImage):
    body = StreamField(CMSStreamBlock())

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

    subpage_types = []

RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    InlinePanel('carousel_items', label='Carousel items'),
    StreamFieldPanel('body'),
    InlinePanel('related_links', label='Related links'),
]

RichTextPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


def _paginate(request, items):
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    return page


# Blogs
# BlogIndexPage
class BlogIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('BlogIndexPage', related_name='related_links')


class BlogIndexPage(RoutablePageMixin, Page, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        # gets list of live blog posts that are descendants of this page
        posts = BlogPost.objects.live().descendant_of(self)

        # orders by most recent date first
        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts
        logger.debug('Posts: {}'.format(posts))

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^author/(?P<author>[\w ]+)/$')
    def author(self, request, author=None):
        if not author:
            # Invalid author filter
            logger.error('Invalid author filter')
            return self.all_posts(request)

        posts = self.posts.filter(owner__username=author)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'author', 'filter': author
            }
        )

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )

BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('intro'),
    InlinePanel('related_links', label='Related links'),
]

BlogIndexPage.promote_panels = Page.promote_panels


# BlogPost
class BlogPostCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('BlogPost', related_name='carousel_items')


class BlogPostRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('BlogPost', related_name='related_links')


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items')


class BlogPost(Page, WithFeedImage, WithStreamField):
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    date = models.DateField('Post date')

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = []

    @property
    def blog_index(self):
        # finds closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label='Carousel items'),
    InlinePanel('related_links', label='Related links'),
]

BlogPost.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]


# Events
# EventIndexPage
class EventIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('EventIndexPage', related_name='related_links')


class EventIndexPage(RoutablePageMixin, Page, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['EventPage']

    @property
    def all_events(self):
        # gets list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)
        events = events.order_by('-date_from')

        return events

    @property
    def live_events(self):
        # gets list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # filters events list to get ones that are either
        # running now or start in the future
        today = date.today()
        events = events.filter(Q(date_from__gte=today) | Q(date_to__gte=today))
        events = events.order_by('date_from')

        return events

    @property
    def past_events(self):
        # gets list of live event pages that are descendants of this page
        events = self.all_events

        today = date.today()
        events = events.filter(Q(date_from__lte=today) | Q(date_to__lte=today))

        return events

    @route(r'^$', name='live_events')
    def get_live_events(self, request):
        events = self.live_events
        logger.debug('Live events: {}'.format(events))

        return render(request, self.get_template(request),
                      {'self': self, 'events': _paginate(request, events)})

    @route(r'^past/$', name='past_events')
    def get_past_events(self, request):
        events = self.past_events
        logger.debug('Past events: {}'.format(events))

        return render(request, self.get_template(request),
                      {'self': self, 'filter_type': 'past',
                       'events': _paginate(request, events)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.get_live_events(request)

        posts = self.all_events.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'events': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )

EventIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('intro'),
    InlinePanel('related_links', label='Related links'),
]

EventIndexPage.promote_panels = Page.promote_panels


# EventPage
class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('EventPage', related_name='tagged_items')


class EventPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('EventPage', related_name='carousel_items')


class EventPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('EventPage', related_name='related_links')


class EventPage(Page, WithFeedImage, WithStreamField):
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)
    date_from = models.DateField('Start date')
    date_to = models.DateField(
        'End date', null=True, blank=True,
        help_text='Not required if event is on a single day'
    )
    time_from = models.TimeField('Start time', null=True, blank=True)
    time_to = models.TimeField('End time', null=True, blank=True)
    location = models.CharField(max_length=256)
    signup_link = models.URLField(null=True, blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('location'),
        index.SearchField('body'),
    )

    subpage_types = []

    @property
    def event_index(self):
        # finds closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

EventPage.content_panels = [
    FieldPanel('title', classname='full title'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('date_from', classname='col6'),
            FieldPanel('date_to', classname='col6'),
        ], classname='full'),
        FieldRowPanel([
            FieldPanel('time_from', classname='col6'),
            FieldPanel('time_to', classname='col6'),
        ], classname='full'),
    ], 'Dates'),
    FieldPanel('location'),
    InlinePanel('carousel_items', label='Carousel items'),
    StreamFieldPanel('body'),
    FieldPanel('signup_link'),
    InlinePanel('related_links', label='Related links'),
]

EventPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]


@receiver(pre_save, sender=EventPage)
def event_page_default_date_to(sender, instance, **kwargs):
    # checks the date to is empty
    if not instance.date_to:
        # sets date_to to the same as date_from
        instance.date_to = instance.date_from


# Symposium
# SymposiumIndexPage
class SymposiumIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('SymposiumIndexPage', related_name='related_links')


class SymposiumIndexPage(RoutablePageMixin, Page, WithIntroduction):
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['SymposiumPage']

    @property
    def symposiums(self):
        symposiums = SymposiumPage.objects.live().descendant_of(self)
        symposiums = symposiums.order_by('-date_from')

        return symposiums

    @route(r'^$', name='all_symposiums')
    def get_all_symposiums(self, request):
        symposiums = self.symposiums
        logger.debug('Live symposiums: {}'.format(symposiums))

        return render(request, self.get_template(request),
                      {'self': self,
                       'symposiums': _paginate(request, symposiums)})

SymposiumIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('intro'),
    InlinePanel('related_links', label='Related links'),
]

EventIndexPage.promote_panels = Page.promote_panels


# SymposiumPage
class SymposiumPageCarouselItem(Orderable, AbstractCarouselItem):
    page = ParentalKey('SymposiumPage', related_name='carousel_items')


class SymposiumPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('SymposiumPage', related_name='related_links')


class SymposiumPage(Page, WithFeedImage, WithStreamField):
    date_from = models.DateField('Start date')
    date_to = models.DateField('End date')
    time_from = models.TimeField('Start time', null=True, blank=True)
    time_to = models.TimeField('End time', null=True, blank=True)
    location = models.CharField(max_length=256)
    signup_link = models.URLField(null=True, blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('location'),
        index.SearchField('body'),
    )

    subpage_types = []

    @property
    def symposium_index(self):
        # finds closest ancestor which is a symposium index
        return self.get_ancestors().type(SymposiumIndexPage).last()

SymposiumPage.content_panels = [
    FieldPanel('title', classname='full title'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('date_from', classname='col6'),
            FieldPanel('date_to', classname='col6'),
        ], classname='full'),
        FieldRowPanel([
            FieldPanel('time_from', classname='col6'),
            FieldPanel('time_to', classname='col6'),
        ], classname='full'),
    ], 'Dates'),
    FieldPanel('location'),
    InlinePanel('carousel_items', label='Carousel items'),
    StreamFieldPanel('body'),
    FieldPanel('signup_link'),
    InlinePanel('related_links', label='Related links'),
]

SymposiumPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


@receiver(pre_save, sender=SymposiumPage)
def symposium_page_efault_date_to(sender, instance, **kwargs):
    # checks the date to is empty
    if not instance.date_to:
        # sets date_to to the same as date_from
        instance.date_to = instance.date_from
