import sys

from bson.objectid import ObjectId
from celery import Celery
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from constants import MONGO_URI, BROKER_URI

from mongo_db import get_mongo_db_connection, get_query_condition

load_dotenv()
client = get_mongo_db_connection()
app = Flask(__name__)

task_manager = Celery('simple_worker', broker=BROKER_URI, backend=MONGO_URI)


@app.route('/v1/material', methods=['POST'])
def add_material():
    try:
        data = request.get_json()

        if 'client_id' not in data or 'formula' not in data or 'density' not in data:
            return jsonify({"error": "Invalid request"}), 400

        client_id = data['client_id']
        # TODO Validate chemical elements are valid in formula
        formula = data['formula']
        density = data['density']

        materialdb = client.materialdb
        materials = materialdb.materials
        existing_material = materials.find_one({'client_id': client_id, "formula": formula, "density": density})

        if existing_material:
            return jsonify({"material_id": str(existing_material["_id"])}), 200
        else:
            new_material = materials.insert_one({'client_id': client_id,
                                                 'formula': formula,
                                                 'density': density})

            return jsonify({"material_id": str(new_material.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/v1/material/<material_id>', methods=['GET'])
def get_material(material_id):
    try:
        material_object_id = ObjectId(material_id)
        materialdb = client.materialdb
        materials = materialdb.materials
        material = materials.find_one(material_object_id)
        del material['_id']

        if material:
            return jsonify(material), 200
        else:
            return jsonify({'error': "Material not found"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/v1/search', methods=['GET'])
def search_material():
    args = request.args

    if len(args) == 0:
        return jsonify({"error": "Invalid request"}), 400

    minimal_density = float(args.get('minimal_density')) if 'minimal_density' in args else None
    maximal_density = float(args.get('maximal_density')) if 'maximal_density' in args else None
    exclude_elements = set(args.get('exclude_elements').split(',')) if 'exclude_elements' in args else []
    include_elements = set(args.get('include_elements').split(',')) if 'include_elements' in args else []
    query_condition = get_query_condition(minimal_density, maximal_density, exclude_elements, include_elements)

    try:
        materialdb = client.materialdb
        materials = materialdb.materials
        records = materials.find({'$and': query_condition})
        return jsonify([{**doc, '_id': str(doc['_id'])} for doc in records]), 200

    except Exception as e:
        print('DB error ', e)
        return 'Internal Server Error', 500


@app.route('/v1/calculate', methods=['POST'])
def calculate():
    try:

        args = request.args

        if len(args) == 0 or 'formula' not in args:
            return jsonify({"error": "Invalid request"}), 400

        formula = args['formula']
        print(formula)
        app.logger.info("Invoking CPU Heavy Method")
        spawn_task = task_manager.send_task('tasks.fooness', kwargs={'formula': formula})
        app.logger.info(spawn_task.backend)
        return {'msg': 'message received', 'status_endpoint': f'/v1/calculate_status/{spawn_task.id}'}, 202

    except Exception as e:
        print('DB error ', e)
        return 'Internal Server Error', 500


@app.route('/v1/calculate_status/<task_id>', methods=['GET'])
def current_status(task_id):
    try:
        status = task_manager.AsyncResult(task_id)
        return {'state': status.state, 'result': status.result}, 200
    except Exception as e:
        print('DB error ', e)
        return 'Internal Server Error', 500


if __name__ == '__main__':
    host = sys.argv[1]
    app.run(host=host, port=5000)
