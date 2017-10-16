#!/usr/bin/python

from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
import os

DOMAIN = 'kool.karmalabs.local'
VERSION = 'v1'
NAMESPACE = os.environ['GUITAR_NAMESPACE'] if 'GUITAR_NAMESPACE' in os.environ else 'guitarcenter'
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
        code = 200
    except Exception as e:
        result = {'result': 'failure', 'reason': e.body}
        code = 200
    response = jsonify(result)
    response.status_code = code
    return response


@app.route("/form")
def guitarform():
    return render_template("guitaradd.html", title="Add Your Guitar")


@app.route("/")
def guitarslist():
    """
    display guitars
    """
    crds = client.CustomObjectsApi()
    guitars = crds.list_cluster_custom_object(DOMAIN, VERSION, 'guitars')["items"]
    return render_template("guitarlist.html", title="Guitars", guitars=guitars)


def run():
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    app.run(host="0.0.0.0", port=9000, debug=True)
    run()

if __name__ == '__main__':
    run()
