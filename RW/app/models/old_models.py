from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base  # Импортируем Base из database.py
import bcrypt

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), default='user')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ratings = relationship("Rating", back_populates="client")
    collections = relationship("Collection", back_populates="client")

    # Методы хеширования
    def set_password(self, password: str):
        salt = bcrypt.gensalt(rounds=int(os.getenv("BCRYPT_ROUNDS", 12)))
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

class Genre(Base):
    __tablename__ = 'genres'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    description = Column(String(200), default='No description')

    objects = relationship("Object", back_populates="genre")

class Object(Base):
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    year = Column(Integer)
    description = Column(String(500))
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete="SET NULL"))
    
    genre = relationship("Genre", back_populates="objects")
    ratings = relationship("Rating", back_populates="object")
    collection_associations = relationship("CollectionObject", back_populates="object")

class Rating(Base):
    __tablename__ = 'ratings'
    
    client_id = Column(Integer, ForeignKey('clients.id', ondelete="CASCADE"), primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id', ondelete="CASCADE"), primary_key=True)
    rating = Column(Integer)
    rated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    client = relationship("Client", back_populates="ratings")
    object = relationship("Object", back_populates="ratings")

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 10', name='check_rating_range'),
    )

class Collection(Base):
    __tablename__ = 'collections'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete="CASCADE"))
    name = Column(String(50), default='My Collection')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    client = relationship("Client", back_populates="collections")
    object_associations = relationship("CollectionObject", back_populates="collection")

class CollectionObject(Base):
    __tablename__ = 'collection_objects'
    
    collection_id = Column(Integer, ForeignKey('collections.id', ondelete="CASCADE"), primary_key=True)
    object_id = Column(Integer, ForeignKey('objects.id', ondelete="CASCADE"), primary_key=True)
    
    collection = relationship("Collection", back_populates="object_associations")
    object = relationship("Object", back_populates="collection_associations")