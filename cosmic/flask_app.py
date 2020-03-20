from flask import Flask, jsonify, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cosmic import config, model, orm, repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )
    batchref = model.allocate(line=line, batches=batches)
    return jsonify({"batchref": batchref}), 201
