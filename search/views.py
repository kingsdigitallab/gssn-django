from django.shortcuts import render
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query


def search(request):
    # Search
    search_query = request.GET.get('q', None)

    if search_query:
        search_results = Page.objects.live().search(search_query)

        # logs the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
