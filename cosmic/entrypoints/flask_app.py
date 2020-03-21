from flask import Flask, jsonify, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cosmic import config
from cosmic.adapters import orm, repository
from cosmic.domain import model
from cosmic.service_layer import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )
    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201
