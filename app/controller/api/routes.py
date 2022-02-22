from flask import Blueprint, request
from app.controller.api import api_controller

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/dosen', methods=['GET','POST'])
def getDosen():
    if request.method == 'GET':
        return api_controller.getDosen()
    else:
        return api_controller.setDosen()

@api.route('/dosen/<id>', methods=['GET','PUT','DELETE'])
def getdetaildosen(id):
    if request.method == 'GET':
        return api_controller.getDosenDetail(id)
    elif request.method == 'PUT':
        return api_controller.update(id)
    else:
        return api_controller.delete(id)