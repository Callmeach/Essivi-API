from pod.extension import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(15), nullable=False)
    prenoms = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True, index=True)
    password = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.Integer, nullable=True, unique=True)
    adresse = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "utilisateurs",
        "polymorphic_on": type
    }

    def __init__(self, nom, prenoms, email, password, telephone, adresse):
        self.nom = nom
        self.prenoms = prenoms
        self.email = email
        self.password = password
        self.telephone = telephone
        self.adresse = adresse
