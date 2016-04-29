from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.assignment_tag(takes_context=False)
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, 'ALLOW_COMMENTS', False)


@register.assignment_tag(takes_context=True)
def get_event_index_page(context):
    """Returns the first event index page available in the current site."""
    site_root = get_site_root(context)
    pages = site_root.get_descendants().live().filter(
        content_type__model='eventindexpage')

    if pages:
        return pages.first().specific

    return None


@register.assignment_tag(takes_context=False)
def get_facebook_url():
    return getattr(settings, 'FACEBOOK_URL')


@register.assignment_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ''
    request = context['request']

    for key, value in request.GET.items():
        if key != exclude:
            params += '&{key}={value}'.format(key=key, value=value)

    return params


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.
    Object-comparison to self will return false as objects would differ.

    :rtype: `wagtail.wagtailcore.models.Page`
    """
    return context['request'].site.root_page


@register.assignment_tag(takes_context=False)
def get_twitter_name():
    return getattr(settings, 'TWITTER_NAME')


@register.assignment_tag(takes_context=False)
def get_twitter_url():
    return getattr(settings, 'TWITTER_URL')


@register.assignment_tag(takes_context=False)
def get_twitter_widget_id():
    return getattr(settings, 'TWITTER_WIDGET_ID')


@register.inclusion_tag('cms/tags/main_menu.html', takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}


@register.filter(name='unslugify')
@stringfilter
def unslugify_filter(value):
    return value.replace('_', ' ').capitalize()
