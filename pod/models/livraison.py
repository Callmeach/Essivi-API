from pod.extension import db
from .agentCommercial import AgentCommercial
from ..models.client import Client


class Livraison(db.Model):
    __tablename__ = 'livraisons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(50), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agents_commerciaux.id'))

    def __init__(self, date, adresse, quantite, status, client, agent):
        self.date = date
        self.adresse = adresse
        self.quantite = quantite
        self.status = status
        self.client_id = client
        self.agent_id = agent

    def livraison_format(self):
        client = Client.query.get(self.client_id)
        agent = AgentCommercial.query.get(self.agent_id)
        return {
            'id': self.id,
            'date': self.date,
            'quantite': self.quantite,
            'adresse': self.adresse,
            'status': self.status,
            'client_id': self.client_id,
            'agent_id': self.agent_id,
            'client': client.client_format(),
            'agent': agent.agent_format()
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
