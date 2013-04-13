from pyramid.view import view_config
from .models import Page


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    one = Page.objects.filter(Page.parent_id == None).one()
    return {'one': one, 'project': 'benben'}
