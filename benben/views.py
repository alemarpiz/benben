from pyramid.view import view_config
from .models import Page


@view_config(context=Page, renderer='templates/page.pt')
def page_view(page, request):
    return {'project': 'benben', 'layout': page.layout}


@view_config(
    route_name='api', context=Page,
    request_method='GET', accept="application/json", renderer='json')
def page_GET(page, request):
    return page
