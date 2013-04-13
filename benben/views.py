from pyramid.view import view_config
from .models import Page


@view_config(context=Page, renderer='templates/page.pt')
def page_view(page, request):
    return {'project': 'benben', 'layout': page.layout}
