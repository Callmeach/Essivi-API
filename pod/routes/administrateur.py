from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash

from ..auth_middleware import token_required
from ..models.administrateur import Administrateur

admin_bp = Blueprint("admin_bp", __name__, url_prefix='/admin')

@admin_bp.get('/')
def get_all_admins():
    admins = [admin.admin_format() for admin in Administrateur.query.all()]

    return jsonify(
        {
            'Administrateurs de Essivi SARL': admins
        }
    )

@admin_bp.get('/current')
@token_required
def get_current_admin(current_user):
    return jsonify(
        {
            'Message': 'Current admin successfully retrieved',
            'admin': current_user.agent_format()
        }
    )

@admin_bp.post('/create')
def create_admin():
    body = request.get_json()

    nom = body.get('nom', None)
    prenoms = body.get('prenoms', None)
    email = body.get('email', None)
    password = generate_password_hash(body.get('password', None))
    telephone = body.get('telephone', None)
    adresse = body.get('adresse', None)

    admin = Administrateur(nom=nom, prenoms=prenoms, email=email, password=password, telephone=telephone,
                           adresse=adresse, active=False)

    admin.insert()

    return jsonify(
        {
            "Administrateur ajouté": admin.admin_format()
        }
    )


@admin_bp.patch('/<int:id>')
def update_admin(id):
    admin = Administrateur.query.get(id)
    if admin is None:
        abort(404)
    else:
        try:
            body = request.get_json()

            admin.nom = body.get('nom')
            admin.prenoms = body.get('prenoms')
            admin.email = body.get('email')
            admin.password = body.get('password')

            admin.update()

            return jsonify(
                {
                    'Administrateur modifié': admin.admin_format()
                }
            )
        except:
            abort(406)


@admin_bp.delete('/<int:id>')
def delete_admin(id):
    admin = Administrateur.query.get(id)
    if admin is None:
        abort(404)
    else:
        admin.delete()
        return jsonify(
            {
                'message': 'Administrateur supprimé avec succès'
            }
        )
