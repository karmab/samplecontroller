#!/usr/bin/python

from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
import os

DOMAIN = 'kool.karmalabs.local'
VERSION = 'v1'
NAMESPACE = os.environ['GUITAR_NAMESPACE'] if 'GUITAR_NAMESPACE' in os.environ else 'guitarcenter'
goodbrands = ['coleclark', 'fender', 'gibson', 'ibanez', 'martin', 'seagull', 'squier', 'washburn']
badbrands = ['epiphone', 'guild', 'gretsch', 'jackson', 'ovation', 'prs', 'rickenbauer', 'taylor', 'yamaha']

app = Flask(__name__)


@app.route("/guitaradd", methods=['POST'])
def guitaradd():
    name = request.form['name']
    brand = request.form['brand']
    body = {'kind': 'Guitar', 'spec': {'brand': brand, 'review': False}, 'apiVersion': '%s/%s' % (DOMAIN, VERSION), 'metadata': {'name': name, 'namespace': NAMESPACE}}
    crds = client.CustomObjectsApi()
    try:
        crds.create_namespaced_custom_object(DOMAIN, VERSION, NAMESPACE, 'guitars', body)
        result = {'result': 'success'}
        # code = 200
    except Exception as e:
        message = [x.split(':')[1] for x in e.body.split(',') if 'message' in x][0].replace('"', '')
        result = {'result': 'failure', 'reason': message}
        # code = e.status
    response = jsonify(result)
    # response.status_code = code
    return response


@app.route("/guitarform")
def guitarform():
    return render_template("guitarform.html", title="Add Your Guitar", brands=sorted(goodbrands + badbrands))


@app.route("/")
def guitarlist():
    """
    display guitars
    """
    crds = client.CustomObjectsApi()
    guitars = crds.list_cluster_custom_object(DOMAIN, VERSION, 'guitars')["items"]
    guitars = sorted(guitars, key=lambda x: (x.get("spec")["brand"], x.get("metadata")["name"]))
    return render_template("guitarlist.html", title="Guitars", guitars=guitars)


def run():
    if 'KUBERNETES_PORT' in os.environ:
        os.environ['KUBERNETES_SERVICE_HOST'] = 'kubernetes'
        config.load_incluster_config()
    else:
        config.load_kube_config()
    app.run(host="0.0.0.0", port=9000)
    run()

if __name__ == '__main__':
    run()
