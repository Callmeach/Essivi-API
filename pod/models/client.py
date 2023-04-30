from pod.extension import db
from .utilisateur import Utilisateur


class Client(Utilisateur):
    __tablename__='clients'
    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)
    adresse_livraison = db.Column(db.String(100), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents_commerciaux.id'))

    __mapper_args__ = {
        "polymorphic_identity": "clients"
    }

    def __init__(self, nom, prenoms, email, password, telephone, adresse, adresse_livraison, agent):
        Utilisateur.__init__(self, nom, prenoms, email, password, telephone, adresse)
        self.adresse_livraison = adresse_livraison
        self.agent_id = agent

    def client_format(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenoms': self.prenoms,
            'email': self.email,
            'telephone': self.telephone,
            'password': self.password,
            'adresse': self.adresse,
            'adresse_livraison': self.adresse_livraison,
            'agent_id': self.agent_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
