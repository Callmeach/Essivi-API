from pod.extension import db
from .utilisateur import Utilisateur


class AgentCommercial(Utilisateur):
    __tablename__='agents_commerciaux'
    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('administrateurs.id'))

    __mapper_args__ = {
        "polymorphic_identity": "agents_commerciaux"
    }

    def __init__(self, nom, prenoms, email, password, telephone, adresse, admin):
        Utilisateur.__init__(self, nom, prenoms, email, password, telephone, adresse)
        self.admin_id = admin

    def agent_format(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenoms': self.prenoms,
            'email': self.email,
            'password': self.password,
            'telephone': self.telephone,
            'adresse': self.adresse,
            'admin_id': self.admin_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
