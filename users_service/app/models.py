from . import db, bcrypt

class User(db.Model):
    """
    User database model.
    Stores user credentials with bcrypt-hashed passwords.
    """
    __tablename__ = 'user' 
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """
        Generate and store bcrypt password hash.
        Should be called before saving the user to the database.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Verify if provided password matches the stored hash.
        Returns True if valid, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'