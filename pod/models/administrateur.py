from pod.extension import db
from .utilisateur import Utilisateur


class Administrateur(Utilisateur):
    __tablename__ = 'administrateurs'
    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)
    is_active = db.Column(db.Boolean, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "administrateurs"
    }

    def __init__(self, nom, prenoms, email, password, telephone, adresse, active):
        Utilisateur.__init__(self, nom, prenoms, email, password, telephone, adresse)
        self.is_active = active

    def admin_format(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenoms': self.prenoms,
            'email': self.email,
            'password': self.password,
            'telephone': self.telephone,
            'adresse': self.adresse,
            'active': self.is_active
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
