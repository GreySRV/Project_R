from app.extensions import db
import bcrypt

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Связи с каскадами
    ratings = db.relationship(
        "Rating", 
        back_populates="client",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    collections = db.relationship(
        "Collection",
        back_populates="client",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())