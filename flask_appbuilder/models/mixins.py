import re
import uuid
import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import sqlalchemy.types as types
from sqlalchemy.types import String
from flask import g


_camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')

class FileColumn(types.TypeDecorator):
    """
    Extends SQLA to support a File Column
    usefull to auto form generation.
    
    """
    impl = types.Text
    

class ImageColumn(types.TypeDecorator):
    impl = types.Text



class BaseMixin(object):
    __table_args__ = {'extend_existing': True}

    @declared_attr
    def __tablename__(cls):
        def _join(match):
            word = match.group()
            if len(word) > 1:
                return ('_%s_%s' % (word[:-1], word[-1])).lower()
            return '_' + word.lower()
        print "NEW", _camelcase_re.sub(_join, cls.__name__).lstrip('_')
        return _camelcase_re.sub(_join, cls.__name__).lstrip('_')
            

class AuditMixin(BaseMixin):
    """
    AuditMixin
    Mixin for models, add 4 cols to stamp, time and user on
    creation and modification
    """
    created_on = Column(DateTime, default=datetime.datetime.now,nullable=False)
    changed_on = Column(DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now,nullable=False)

    @declared_attr
    def created_by_fk(cls):
        return Column(Integer, ForeignKey('ab_user.id'),
                default=cls.get_user_id,nullable=False)

    @declared_attr
    def created_by(cls):
        return relationship("User", primaryjoin='%s.created_by_fk == User.id'%cls.__name__)

    @declared_attr
    def changed_by_fk(cls):
        return Column(Integer, ForeignKey('ab_user.id'),
                default=cls.get_user_id,onupdate=cls.get_user_id,nullable=False)

    @declared_attr
    def changed_by(cls):
        return relationship("User", primaryjoin='%s.changed_by_fk == User.id'%cls.__name__)


    @classmethod
    def get_user_id(cls):
        return g.user.id
