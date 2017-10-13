import json
from kubernetes import client, config, watch
# import logging

DOMAIN = "kool.karmalabs.local"


def review_guitar(crds, event, obj):
    metadata = obj.get("metadata")
    goodguitars = ['fender', 'martin']
    if not metadata:
        # logging.error("No metadata in object, skipping: %s", json.dumps(obj, indent=1))
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["review"] = True
    brand = obj["spec"]["brand"]
    if brand in goodguitars:
        obj["spec"]["comment"] = "this is a great instrument"
    else:
        obj["spec"]["comment"] = "this is shit"

    # logging.info("Updating: %s", name)
    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "guitars", name, obj)


if __name__ == "__main__":
    # config.load_kube_config()
    config.load_incluster_config()
    namespace = "default"
    crds = client.CustomObjectsApi()

    print("Waiting for Guitars to come up...")
    # logging.info("Waiting for Guitars to come up...")
    stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "guitars")
    for event in stream:
        obj = event["object"]
        spec = obj.get("spec")
        if not spec:
            print("No 'spec' in object, skipping event: %s" % json.dumps(obj, indent=1))
            # logging.error("No 'spec' in object, skipping event: %s", json.dumps(obj, indent=1))
            continue
        done = spec.get("review", False)
        if done:
            continue
        review_guitar(crds, event, obj)
