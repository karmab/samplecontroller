import json
from kubernetes import client, config, watch
import os


def review_event(obj):
    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    print(name)


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    print("Waiting for Events to come up...")
    v1 = client.CoreV1Api()
    resource_version = ''
    while True:
        stream = watch.Watch().stream(v1.list_event_for_all_namespaces)
        for event in stream:
            obj = event["object"]
            message = obj.message
            metadata = obj.metadata
            operation = event["type"]
            # resource_version = metadata['resourceVersion']
            print message
            # review_event(obj)
