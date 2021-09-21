from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), default="")
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', cascade="all, delete", backref='user', uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
   
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False) 
    height = db.Column(db.String(250), default="")
    mass = db.Column(db.String(250), default="")
    hair_color = db.Column(db.String(250), default="")
    skin_color = db.Column(db.String(250), default="")
    eye_color = db.Column(db.String(250), default="")
    birth_year = db.Column(db.String(250), default="")
    gender = db.Column(db.String(250), default="")
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete="CASCADE"))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False) 
    diameter = db.Column(db.String(250), default="")
    population = db.Column(db.String(250), default="")
    climate = db.Column(db.String(250), default="")
    terrain = db.Column(db.String(250), default="")
    surface_water = db.Column(db.String(250), default="")
    gravity = db.Column(db.String(250), default="")
    rotation_period = db.Column(db.String(250), default="")
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete="CASCADE"))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "gravity": self.gravity,
            "rotation_period": self.rotation_period
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    planets = db.relationship('Planet', cascade="all, delete", backref="favorites")
    people = db.relationship('People', cascade="all, delete", backref="favorites")

    def serialize(self):
        return {
            "id": self.id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
   
    








# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }