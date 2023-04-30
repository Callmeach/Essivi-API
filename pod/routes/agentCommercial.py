from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash

from ..auth_middleware import token_required
from ..models.agentCommercial import AgentCommercial

agent_bp = Blueprint("agent_bp", __name__, url_prefix='/agents')

agent_default_password = '0000'


@agent_bp.get('/')
@token_required
def get_all_agents():
    agents = [agent.agent_format() for agent in AgentCommercial.query.all()]

    return jsonify(
        {
            "agents": agents,
            "total": len(agents)
        }
    )


@agent_bp.get('/<int:id>')
def get_an_agent(id):
    agent = AgentCommercial.query.get(id)
    if agent is None:
        abort(404)
    else:
        return jsonify(
            {
                "Agent": agent.agent_format()
            }
        )


@agent_bp.post('/create')
@token_required
def create_agent(current_user):
    body = request.get_json()

    nom = body.get('nom', None)
    prenoms = body.get('prenoms', None)
    email = body.get('email', None)
    password = generate_password_hash(agent_default_password)
    telephone = body.get('telephone', None)
    adresse = body.get('adresse', None)
    admin_id = current_user.id

    agent = AgentCommercial(nom=nom, prenoms=prenoms, email=email, password=password,
                            telephone=telephone, adresse=adresse, admin=admin_id)

    agent.insert()

    return jsonify(
        {
            "Agent Commercial ajouté": agent.agent_format()
        }
    )


@agent_bp.patch('/<int:id>')
def update_agent(id):
    agent = AgentCommercial.query.get(id)
    if agent is None:
        abort(404)
    else:
        try:
            body = request.get_json()

            agent.nom = body.get('nom')
            agent.prenoms = body.get('prenoms')
            agent.email = body.get('email')
            agent.password = body.get('password')
            agent.telephone = body.get('telephone')
            agent.adresse = body.get('adresse')

            agent.update()

            return jsonify(
                {
                    'Agent Commercial modifié': agent.agent_format()
                }
            )
        except:
            abort(406)


@agent_bp.delete('/<int:id>')
def delete_agent(id):
    agent = AgentCommercial.query.get(id)
    if agent is None:
        abort(404)
    else:
        agent.delete()
        return jsonify(
            {
                'message': 'Agent Commercial supprimé avec succès'
            }
        )
