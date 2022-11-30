from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

usuario_planeta = db.Table('usuario_planeta',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('planeta_id', db.Integer, db.ForeignKey('planeta.id'))
)

usuario_personaje = db.Table('usuario_personaje',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('personaje_id', db.Integer, db.ForeignKey('personaje.id'))
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    followingPlaneta = db.relationship('Planeta', secondary=usuario_planeta, backref='followerPlaneta')
    followingPersonaje = db.relationship('Personaje', secondary=usuario_personaje, backref='followerPersonaje')

    def __repr__(self):
        return '<Usuario %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "password": self.password,
            # do not serialize the password, its a security breach
        }

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    rutaimagen = db.Column(db.String(250), nullable=False)
    habitantes = db.Column(db.Integer, nullable=False)
    terreno = db.Column(db.String(250), nullable=False)
    clima = db.Column(db.String(100), nullable=False)
    periodoOrbita = db.Column(db.Integer, nullable=False)
    periodoRotacion = db.Column(db.Integer, nullable=False)
    diametro = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Planeta %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rutaimagen": self.rutaimagen,
            "habitantes": self.habitantes,
            "terreno": self.terreno,
            "clima": self.clima,
            "periodoOrbita": self.periodoOrbita,
            "periodoRotacion": self.periodoRotacion,
            "diametro": self.diametro,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    rutaimagen = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    colorpelo = db.Column(db.String(20), nullable=False)
    colorojos = db.Column(db.String(20), nullable=False)
    nacimiento = db.Column(db.String(100), nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    colorpiel = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Personaje %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rutaimagen": self.rutaimagen,
            "genero": self.genero,
            "colorpelo": self.colorpelo,
            "colorojos": self.colorojos,
            "nacimiento": self.nacimiento,
            "altura": self.altura,
            "colorpiel": self.colorpiel,
            # do not serialize the password, its a security breach
        }
