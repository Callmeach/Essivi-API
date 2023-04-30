from flask import Blueprint, request, jsonify, abort, current_app
from werkzeug.security import generate_password_hash

from ..auth_middleware import token_required
from ..models.client import Client

client_bp = Blueprint("client_bp", __name__, url_prefix='/clients')

client_default_password = '0000'

@client_bp.get('/')
@token_required
def get_all_clients():
    clients = [client.client_format() for client in Client.query.all()]

    return jsonify(
        {
            "clients": clients,
            "total": len(clients)
        }
    )


@client_bp.get('/<int:id>')
def get_a_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        return jsonify(
            {
                'Client': client.client_format()
            }
        )

@client_bp.get('/me')
@token_required
def get_an_agent_clients_list(current_user):
    clients = Client.query.filter_by(agent_id = current_user.id)
    clientList = [client.client_format() for client in clients]

    return jsonify(
        {
            "Liste": clientList
        }
    )

@client_bp.get('/agent/<int:id_>/all')
@token_required
def get_an_agent_clients_list_by_his_id(id_):
    clients = Client.query.filter_by(agent_id = id_)
    clients_list = [client.client_format() for client in clients]

    return jsonify(
        {
            "Liste" : clients_list
        }
    )

@client_bp.get('/not-delivered')
def get_non_delivered_clients():
    clients = Client.query.filter_by(agent_id = None)
    clientsList = [client.client_format() for client in clients]

    return jsonify(
        {
            "Liste des clients n'ayant pas de livreurs": clientsList
        }
    )

@client_bp.patch('/<int:id>/agent/add')
@token_required
def assign_agent_to_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        try:
            body = request.get_json()
            agent_id = body.get(id)

            client.agent_id = agent_id

            return jsonify(
                {
                    "Agent commercial" + agent_id + "affecté au client" + client.id
                }
            )
        except Exception as e:
            current_app.aborter(404, str(e))


@client_bp.post('/create')
@token_required
def create_client(current_user):
    body = request.get_json()

    nom = body.get('nom', None)
    prenoms = body.get('prenoms', None)
    email = body.get('email', None)
    password = body.get('password', generate_password_hash(client_default_password))
    telephone = body.get('telephone', None)
    adresse = body.get('adresse', None)
    adresse_livraison = body.get('adresse_livraison', 'Lome')
    agent_id = body.get('agent_id', current_user.id)

    client = Client(nom=nom, prenoms=prenoms, email=email, password=password,telephone=telephone,
                    adresse=adresse, adresse_livraison=adresse_livraison, agent=agent_id)

    client.insert()

    return jsonify(
        {
            "Client ajouté": client.client_format(),
            "success_message": "Bravo pour ton premier client!!!"
        }
    )


@client_bp.patch('/<int:id>')
def update_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        try:
            body = request.get_json()

            client.nom = body.get('nom')
            client.prenoms = body.get('prenoms')
            client.email = body.get('email')
            client.telephone = body.get('telephone')
            client.adresse = body.get('adresse')
            client.adresse_livraison = body.get('adresse_livraison')

            client.update()

            return jsonify(
                {
                    'Client modifié': client.agent_format()
                }
            )
        except:
            abort(406)


@client_bp.delete('/<int:id>')
def delete_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        client.delete()
        return jsonify(
            {
                'message': "Client supprimé avec succès"
            }
        )
