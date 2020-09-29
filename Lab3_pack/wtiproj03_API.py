from flask import Flask, jsonify, abort, request, make_response
import json
from wtiproj03_ETL import PMovies # Taki import dziala dzieki __init__.py

pm = PMovies()
pivoted = pm.getPivotAllTable()


app = Flask(__name__, static_url_path="")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/ratings', methods=['DELETE'])
def ratings():
    return jsonify({}), 200, {"Content-Type": "application/json"}


@app.route('/ratings', methods=["GET"])
def xx():
    ret = []
    for index, row in pivoted.iterrows():
        if index < 100:
            ret.append(json.loads(row.to_json(orient='columns')))
        else:
            break
    return jsonify(ret), 200, {"Content-Type": "application/json"}


@app.route('/rating', methods=['POST'])
def rating():
    result = request.get_json()
    return jsonify(result), 200, {"Content-Type": "application/json"}


@app.route('/avg-genre-ratings/<userID>', methods=["GET"])
def avg_user(userID):
    ret = []
    for index, row in pm.getPivotUser(int(userID)).iterrows():
        ret.append(json.loads(row.to_json(orient='columns')))

    return jsonify(ret[0]), 200, {"Content-Type": "application/json"}


@app.route('/avg-genre-ratings/all-users', methods=["GET"])
def all_users():
    ret = []
    for index, row in pm.getAvg().iterrows():
        ret.append(json.loads(row.to_json(orient='columns')))

    return jsonify(ret[0]), 200, {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
