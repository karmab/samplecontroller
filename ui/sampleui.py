#!/usr/bin/python

from flask import Flask, render_template
from kubernetes import client, config
import os

DOMAIN = "kool.karmalabs.local"
app = Flask(__name__)


@app.route("/add")
def guitaradd():
    return render_template("add.html", title="Add Your Guitar")


@app.route("/")
def guitarslist():
    """
    display guitars
    """
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    crds = client.CustomObjectsApi()
    guitars = crds.list_cluster_custom_object(DOMAIN, "v1", "guitars")["items"]
    return render_template("index.html", title="Guitars", guitars=guitars)


def run():
    app.run(host="0.0.0.0", port=9000)
    run()

if __name__ == '__main__':
    run()
