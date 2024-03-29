from cms.models.pages import _paginate
from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):
    # Search
    search_query = request.GET.get('q', None)

    if search_query:
        queryset = Page.objects.live().search(search_query)

        # logs the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        queryset = Page.objects.none()

    search_results = _paginate(request, queryset)

    # Render template
    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
