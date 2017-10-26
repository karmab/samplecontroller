import json
# import yaml
from kubernetes import client, config, watch
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
    # labels = metadata.labels
    annotations = metadata.annotations
    if initializers is None:
        return
    for entry in initializers.pending:
        if entry.name == INITIALIZER:
            print("Updating deployment %s" % name)
            initializers.pending.remove(entry)
            if not initializers.pending:
                initializers = None
            obj.metadata.initializers = initializers
            if annotation is None or (annotations and annotation in annotations and annotations[annotation] == 'true'):
                print("Adding container %s to deployment %s" % (inject, name))
                newcontainer = {'image': inject, 'name': 'injected'}
                obj.spec.template.spec.containers.append(newcontainer)
            v1.replace_namespaced_deployment(name, namespace, obj)
            break


if __name__ == "__main__":
    global v1
    inject = os.environ['INJECT_POD'] if 'INJECT_POD' in os.environ else 'karmab/kdummy'
    annotation = os.environ['ANNOTATION'] if 'ANNOTATION' in os.environ else None
    if annotation is not None:
        print "Injecting %s to new deployments with annotation %s set to true" % (inject, annotation)
    else:
        print "Injecting %s to all new deployments" % inject
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
        definition = '/tmp/guitar.yml'
    else:
        config.load_kube_config()
        definition = 'guitar.yml'
    v1 = client.AppsV1beta1Api()
    resource_version = ''
    while True:
        stream = watch.Watch().stream(v1.list_deployment_for_all_namespaces, include_uninitialized=True, resource_version=resource_version)
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
