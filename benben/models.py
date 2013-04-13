from abc import ABCMeta
from benben.sqla import (
    NestedMutationDict,
    JsonType,
    )
try:
    from collections import MutableMapping
except ImportError:
    from UserDict import DictMixin as MutableMapping
from pyramid.traversal import resource_path
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Unicode,
    UniqueConstraint,
    )
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import (
    backref,
    relation,
    scoped_session,
    sessionmaker,
    )
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import (
    and_,
    select,
    )
from zope.sqlalchemy import ZopeTransactionExtension
import os
import transaction

metadata = MetaData()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Base.metadata = metadata
Base.objects = DBSession.query_property()


class PageMetaclass(DeclarativeMeta, ABCMeta):
    # grumble, without this we get a metaclass conflict
    pass


class Page(Base, MutableMapping, metaclass=PageMetaclass):
    """A basic page in the content hierarchy."""

    __tablename__ = 'pages'
    __table_args__ = (
        UniqueConstraint('parent_id', 'name'),
        )
    __mapper_args__ = dict(
        polymorphic_on='type',
        polymorphic_identity='page',
        with_polymorphic='*',
        )

    #: Primary key for the page in the DB
    #: (:class:`sqlalchemy.types.Integer`)
    id = Column(Integer(), primary_key=True, autoincrement=True)
    #: Lowercase class name of the page instance
    #: (:class:`sqlalchemy.types.String`)
    type = Column(String(30), nullable=False)
    #: ID of the page's parent
    #: (:class:`sqlalchemy.types.Integer`)
    parent_id = Column(ForeignKey('pages.id'))
    #: Position of the page within its container / parent
    #: (:class:`sqlalchemy.types.Integer`)
    position = Column(Integer())
    #: Name of the page as used in the URL
    #: (:class:`sqlalchemy.types.Unicode`)
    name = Column(Unicode(50), nullable=False)
    #: Title of the page, e.g. as shown in search results
    #: (:class:`sqlalchemy.types.Unicode`)
    title = Column(Unicode(100))
    #: JSON representing the page's layout
    #: (:class:`benben.sqla.NestedMutationDict`)
    layout = Column(NestedMutationDict.as_mutable(JsonType))

    _children = relation(
        'Page',
        collection_class=ordering_list('position'),
        order_by=[position],
        backref=backref('parent', remote_side=[id]),
        cascade='all',
        )

    def __init__(self, name=None, parent=None, title=u"", layout=None):
        """Constructor"""
        self.name = name
        self.parent = parent
        self.title = title
        if layout is None:
            layout = {}
        self.layout = layout

    @property
    def __name__(self):
        return self.name

    @property
    def __parent__(self):
        return self.parent

    @__parent__.setter
    def __parent__(self, value):
        self.parent = value

    def __repr__(self):
        return '<%s %s at %s>' % (
            self.__class__.__name__, self.id, resource_path(self))

    def __eq__(self, other):
        return isinstance(other, Page) and self.id == other.id

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.id)

    # Container API

    def __setitem__(self, key, page):
        key = page.name = unicode(key)
        self.children.append(page)

    def __delitem__(self, key):
        page = self[unicode(key)]
        self.children.remove(page)
        DBSession.delete(page)

    def keys(self):
        """
        :result: A list of children names.
        :rtype: list
        """

        return [child.name for child in self.children]

    def __getitem__(self, path):
        DBSession()._autoflush()

        if not hasattr(path, '__iter__'):
            path = (path,)
        path = [unicode(p) for p in path]

        # Optimization: don't query children if self._children already there:
        if '_children' in self.__dict__:
            first, rest = path[0], path[1:]
            try:
                [child] = filter(lambda ch: ch.name == path[0], self._children)
            except ValueError:
                raise KeyError(path)
            if rest:
                return child[rest]
            else:
                return child

        if len(path) == 1:
            try:
                return Page.objects.filter_by(
                    name=path[0], parent=self).one()
            except NoResultFound:
                raise KeyError(path)

        # We have a path with more than one element, so let's be a
        # little clever about fetching the requested page:
        pages = Page.__table__
        conditions = [pages.c.id == self.id]
        alias = pages
        for name in path:
            alias, old_alias = pages.alias(), alias
            conditions.append(alias.c.parent_id == old_alias.c.id)
            conditions.append(alias.c.name == name)
        expr = select([alias.c.id], and_(*conditions))
        row = DBSession.execute(expr).fetchone()
        if row is None:
            raise KeyError(path)
        return Page.objects.get(row.id)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    @hybrid_property
    def children(self):
        """Return *all* child pages without considering permissions."""
        return self._children


def get_root(request=None):
    """Get the root page.

    :param request: Current request (optional)
    :type request: :class:`pyramid.request.Request`

    :result: Page in the tree that has no parent.
    :rtype: :class:`~benben.models.Page` or descendant; in a fresh Benben site
            this will be an instance of :class:`~benben.models.Page`.
    """
    return Page.objects.filter(Page.parent_id == None).one()


def populate():
    """
    Create the root page (:class:`~benben.models.Page`)
    if there are no pages in the tree yet.
    """

    if Page.objects.count() == 0:
        DBSession.add(Page(name=u'root', title=u'Benben'))


def initialize_sql(engine, drop_all=False):
    DBSession.registry.clear()
    DBSession.configure(bind=engine)
    metadata.bind = engine

    if drop_all or os.environ.get('BENBEN_TEST_DB_STRING'):
        metadata.reflect()
        metadata.drop_all(engine)

    metadata.create_all(engine)
    populate()
    transaction.commit()

    return DBSession
