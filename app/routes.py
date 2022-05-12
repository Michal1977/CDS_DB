from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from app.models import DbCdLibrary
from json_models import JsonCdLibrary
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app import app


cds = DbCdLibrary()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/bands/", methods=["GET"])
def bands_list():
    return jsonify(cds.all_bands())


@app.route("/api/v1/bands/", methods=["POST"])
def create_band():    

    if not request.json or not 'name' in request.json:
        abort(400)

    if cds.get_band_by_name(request.json['name']) is not None:
        abort(400)

    created = cds.create_band(request.json['name'])
    
    return jsonify({ 'band': created }), 201


@app.route("/api/v1/cds/", methods=["GET"])
def cds_list_api_v1():
    return jsonify(cds.all())


@app.route("/api/v1/cds/<int:cd_id>", methods=["GET"])
def get_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    return jsonify({"cd": cd})


@app.route("/api/v1/cds/", methods=["POST"])
def create_cd():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    created = cds.create(request.json['title'], request.json.get('year', ''), request.json.get('bands', []))
    
    return jsonify({'cd': created}), 201


@app.route("/api/v1/cds/<int:cd_id>", methods=['DELETE'])
def delete_cd(cd_id):
    result = cds.delete(cd_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/cds/<int:cd_id>", methods=["PUT"])
def update_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    if not request.json:
        abort(400)
    
    cd = cds.update(cd_id, request.json['title'], request.json.get('year'), request.json.get('bands'))

    if cd is None: 
        abort(404)
    
    return jsonify({'cd': cd})


# if __name__ == "__main__":
#     app.run(debug=True)