from flask import Blueprint, request, jsonify, abort
from datetime import date, datetime

from ..auth_middleware import token_required
from ..models.client import Client
from ..models.livraison import Livraison

livraison_bp = Blueprint("livraison_bp", __name__, url_prefix='/livraison')

prix_livraison = 500


@livraison_bp.get('/list')
@token_required
def get_all_deliveries_list():
    deliveries = Livraison.query.filter_by(status=True)
    deliveries_list = [delivery.livraison_format() for delivery in deliveries]
    qte_total = 0
    for item in deliveries_list:
        qte_total += item['quantite']

    return jsonify(
        {
            "Livraisons": deliveries_list,
            "Total_Revenu": qte_total * prix_livraison
        }
    )

@livraison_bp.get('/today')
@token_required
def get_today_deliveries_list():
    deliveries = Livraison.query.filter_by(status=True, date=date.today())
    deliveries_list = [delivery.livraison_format() for delivery in deliveries]
    qte_today = 0
    for item in deliveries_list:
        qte_today += item['quantite']

    return jsonify(
        {
            "total": len(deliveries_list),
            "quantite": qte_today,
            "revenu": qte_today * prix_livraison
        }
    )

@livraison_bp.post('/client/<int:_id>/create')
@token_required
def create_livraison(current_user, _id):
    body = request.get_json()

    date_livraison_str = body.get('date_livraison', str(date.today()))
    date_livraison = datetime.strptime(date_livraison_str, '%Y-%m-%d').date()
    adresse = body.get('adresse', "Lome")
    quantite = body.get('quantite', 0)
    client = Client.query.get(_id)
    agent_id = current_user.id

    livraison = Livraison(date=date_livraison, quantite=quantite,adresse=adresse,
                          status=False ,agent=agent_id, client=client.id)

    livraison.insert()

    return jsonify(
        {
            "datas": livraison.livraison_format(),
            "message": "Succes"
        }
    )

@livraison_bp.get('/schedules/me')
@token_required
def get_scheduled_deliveries(current_user):
    livraisons = Livraison.query.filter_by(agent_id=current_user.id, status=False)
    livraisons_schedules = [livraison.livraison_format() for livraison in livraisons]

    return jsonify(
        {
            "Schedules" : livraisons_schedules
        }
    )

@livraison_bp.get('/agent/<int:_id>/all')
@token_required
def get_an_agent_deliveries_list(_id):
    livraisons = Livraison.query.filter_by(agent_id=_id, status=True).order_by(Livraison.date.desc())
    livraisons_list = [livraison.livraison_format() for livraison in livraisons]

    return jsonify(
        {
            "Livraisons" : livraisons_list
        }
    )

@livraison_bp.get('/agent/me/schedules')
@token_required
def get_an_agent_schedules_list(current_user):
    schedules = Livraison.query.filter_by(agent_id=current_user.id, date=date.today())
    schedules_list = [schedule.livraison_format() for schedule in schedules]

    return jsonify(
        {
            "total": len(schedules_list)
        }
    )


@livraison_bp.get('/agent/me/remaining')
@token_required
def get_an_agent__remaining_schedules_list(current_user):
    schedules = Livraison.query.filter_by(agent_id=current_user.id, date=date.today(), status=False)
    schedules_list = [schedule.livraison_format() for schedule in schedules]

    return jsonify(
        {
            "remaining": len(schedules_list)
        }
    )

@livraison_bp.patch('/<int:id>')
def update_livraison(id):
    livraison = Livraison.query.get(id)

    if livraison is None:
        abort(404)
    else:
        try:
            body = request.get_json()

            livraison.adresse = body.get('adresse', None)
            livraison.quantite = body.get('quantite', None)
            livraison.status = True

            livraison.update()

            return jsonify(
                {
                    "Livraison": livraison.livraison_format()
                }
            )
        except:
            abort(406)


@livraison_bp.delete('/<int:id>')
def delete_livraison(id):
    livraison = Livraison.query.get(id)

    if livraison is None:
        abort(404)
    else:
        livraison.delete()

        return jsonify(
            {
                "message": "Livraison annulée avec succès"
            }
        )