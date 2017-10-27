from kubernetes import config
from openshift import client, watch
import os


def process_image(obj):
    metadata = obj.metadata
    name = metadata.name
    namespace = metadata.namespace
    for tag in obj.spec.tags:
        if tag.name == 'latest':
            continue
        else:
            print("Deleting %s:%s" % (name, tag.name))
            oapi.delete_namespaced_image_stream_tag("%s:%s" % (name, tag.name), namespace)
    return


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
        stream = watch.Watch().stream(oapi.list_image_stream_for_all_namespaces, resource_version=resource_version)
        for event in stream:
                obj = event["object"]
                operation = event['type']
                spec = obj.spec
                if not spec:
                    continue
                metadata = obj.metadata
                resource_version = metadata._resource_version
                name = metadata.name
                if operation == 'ADDED':
                    print("Handling %s on %s" % (operation, name))
                    process_image(obj)
