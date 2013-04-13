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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import (
    backref,
    relation,
    scoped_session,
    sessionmaker,
    )
from zope.sqlalchemy import ZopeTransactionExtension
import os
import transaction

metadata = MetaData()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Base.metadata = metadata
Base.objects = DBSession.query_property()


class Page(Base):
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

    #: Primary key for the node in the DB
    #: (:class:`sqlalchemy.types.Integer`)
    id = Column(Integer(), primary_key=True, autoincrement=True)
    #: Lowercase class name of the node instance
    #: (:class:`sqlalchemy.types.String`)
    type = Column(String(30), nullable=False)
    #: ID of the node's parent
    #: (:class:`sqlalchemy.types.Integer`)
    parent_id = Column(ForeignKey('pages.id'))
    #: Position of the node within its container / parent
    #: (:class:`sqlalchemy.types.Integer`)
    position = Column(Integer())
    #: Name of the node as used in the URL
    #: (:class:`sqlalchemy.types.Unicode`)
    name = Column(Unicode(50), nullable=False)
    #: Title of the node, e.g. as shown in search results
    #: (:class:`sqlalchemy.types.Unicode`)
    title = Column(Unicode(100))

    _children = relation(
        'Page',
        collection_class=ordering_list('position'),
        order_by=[position],
        backref=backref('parent', remote_side=[id]),
        cascade='all',
        )

    def __init__(self, name=None, parent=None, title=u""):
        """Constructor"""
        self.name = name
        self.parent = parent
        self.title = title

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
