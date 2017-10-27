import json
from kubernetes import config
from openshift import client, watch
import os


INITIALIZER = 'test.initializer.karmalabs.local'


def process_deployment(obj):
    metadata = obj.metadata
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.name
    initializers = metadata.initializers
    namespace = metadata.namespace
    annotations = metadata.annotations
    if initializers is None:
        return
    for entry in initializers.pending:
        if entry.name == INITIALIZER:
            print("Updating deployment config %s" % name)
            initializers.pending.remove(entry)
            if not initializers.pending:
                initializers = None
            obj.metadata.initializers = initializers
            if annotation is None or (annotations and annotation in annotations and annotations[annotation] == 'true'):
                print("Adding container %s to deployment config %s" % (inject, name))
                newcontainer = {'image': inject, 'name': 'injected'}
                obj.spec.template.spec.containers.append(newcontainer)
            oapi.replace_namespaced_deployment_config(name, namespace, obj)
            break


if __name__ == "__main__":
    global oapi
    inject = os.environ['INJECT_POD'] if 'INJECT_POD' in os.environ else 'karmab/kdummy'
    annotation = os.environ['ANNOTATION'] if 'ANNOTATION' in os.environ else None
    if annotation is not None:
        print "Injecting %s to new deployment configs with annotation %s set to true" % (inject, annotation)
    else:
        print "Injecting %s to all new deployment configs" % inject
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    oapi = client.OapiApi()
    resource_version = ''
    while True:
        stream = watch.Watch().stream(oapi.list_deployment_config_for_all_namespaces, include_uninitialized=True, resource_version=resource_version)
        for event in stream:
                obj = event["object"]
                operation = event['type']
                spec = obj.spec
                if not spec:
                    continue
                metadata = obj.metadata
                resource_version = metadata._resource_version
                name = metadata.name
                print("Handling %s on %s" % (operation, name))
                process_deployment(obj)
