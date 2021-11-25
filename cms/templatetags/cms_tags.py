from cms.models.pages import HomePage
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.dateformat import DateFormat
from django.utils.safestring import mark_safe
from wagtail.core.models import Site

register = template.Library()


@register.simple_tag(takes_context=False)
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, 'ALLOW_COMMENTS', False)


@register.filter(name='date_as_block')
def date_as_block_filter(value):
    df = DateFormat(value)
    result = '''<{0} class="day">{1}</{0}>
        <{0} class="month">{2}</{0}>
        <{0} class="year">{3}</{0}>'''.format(
        'span', df.format('d'), df.format('M'), df.format('Y'))
    return mark_safe(result)


@register.simple_tag(takes_context=True)
def get_blog_index_page(context):
    """Returns the first blog index page available in the current site."""
    site_root = get_site_root(context)
    pages = site_root.get_descendants().live().filter(
        content_type__model='blogindexpage')

    if pages:
        return pages.first().specific

    return None


@register.simple_tag(takes_context=True)
def get_event_index_page(context):
    """Returns the first event index page available in the current site."""
    site_root = get_site_root(context)
    pages = site_root.get_descendants().live().filter(
        content_type__model='eventindexpage')

    if pages:
        return pages.first().specific

    return None


@register.simple_tag(takes_context=False)
def get_facebook_url():
    return getattr(settings, 'FACEBOOK_URL')


@register.simple_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ''
    request = context['request']

    for key, value in list(request.GET.items()):
        if key != exclude:
            params += '&{key}={value}'.format(key=key, value=value)

    return params


@register.simple_tag(takes_context=True)
def get_resources_index_page(context):
    """Returns the first resource index page available in the current site."""
    site_root = get_site_root(context)
    pages = site_root.get_descendants().live().filter(
        content_type__model='resourcesindexpage')

    if pages:
        return pages.first().specific

    return None


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context['request']).root_page


@register.simple_tag(takes_context=False)
def get_twitter_name():
    return getattr(settings, 'TWITTER_NAME')


@register.simple_tag(takes_context=False)
def get_twitter_url():
    return getattr(settings, 'TWITTER_URL')


@register.simple_tag(takes_context=False)
def get_twitter_widget_id():
    return getattr(settings, 'TWITTER_WIDGET_ID')


@register.simple_tag(takes_context=True)
def has_local_menu(context, current_page):
    """Returns True if the current page has a local menu, False otherwise. A
    page has a local menu, if it is not the site root, and if it is not a leaf
    page."""
    site_root = get_site_root(context)

    try:
        current_page.id
    except AttributeError:
        return False

    if current_page.id != site_root.id:
        if current_page.depth >= 3 and not current_page.is_leaf():
            return True
        elif current_page.depth >= 4:
            return True

    return False


@register.inclusion_tag('cms/tags/local_menu.html', takes_context=True)
def local_menu(context, current_page=None):
    """Retrieves the secondary links for the 'also in this section' links -
    either the children or siblings of the current page."""
    label = current_page.title
    menu_pages = []
    menu_root = current_page

    if current_page:
        menu_pages = current_page.get_children().filter(live=True)

        # if no children, get siblings instead
        if len(menu_pages) == 0:
            menu_pages = current_page.get_siblings().filter(live=True)
            menu_root = current_page.get_parent()

        if current_page.get_children_count() == 0:
            if not isinstance(current_page.get_parent().specific, HomePage):
                label = current_page.get_parent().title

    # required by the pageurl tag that we want to use within this template
    return {'request': context['request'], 'current_page': current_page,
            'menu_pages': menu_pages, 'menu_label': label,
            'menu_root': menu_root}


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
