from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Folder(SqlAlchemyBase):
    __tablename__ = 'Folders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    parent_id = Column(Integer, ForeignKey('Folders.id'))
    parent = relationship("Folder", backref="folders", remote_side="Folder.id")
    owner_id = Column(Integer, ForeignKey('Users.id'))
    owner = relationship("User")


class File(SqlAlchemyBase):
    __tablename__ = 'Files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    parent_id = Column(Integer, ForeignKey('Folders.id'))
    parent = relationship("Folder", backref="files", remote_side="Folder.id")
    owner_id = Column(Integer, ForeignKey('Users.id'))
    owner = relationship("User")
