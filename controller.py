import json
import yaml
from kubernetes import client, config, watch
import os

DOMAIN = "kool.karmalabs.local"
goodbrands = ['coleclark', 'fender', 'gibson', 'ibanez', 'martin', 'seagull', 'squier', 'washburn']
badbrands = ['epiphone', 'guild', 'gretsch', 'jackson', 'ovation', 'prs', 'rickenbauer', 'taylor', 'yamaha']


def review_guitar(crds, obj):
    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["review"] = True
    brand = obj["spec"]["brand"]
    if brand in goodbrands:
        obj["spec"]["comment"] = "this is a great instrument"
    elif brand in badbrands:
        obj["spec"]["comment"] = "this is shit"
    else:
        obj["spec"]["comment"] = "nobody knows this brand"

    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "guitars", name, obj)


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
        definition = '/tmp/guitar.yml'
    else:
        config.load_kube_config()
        definition = 'guitar.yml'
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
    if 'guitar' not in current_crds:
        print("Creating guitar definition")
        with open(definition) as data:
            body = yaml.load(data)
        v1.create_custom_resource_definition(body)
    crds = client.CustomObjectsApi(api_client)

    print("Waiting for Guitars to come up...")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "guitars", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            if not spec:
                continue
            metadata = obj.get("metadata")
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            print("Handling %s on %s" % (operation, name))
            done = spec.get("review", False)
            if done:
                continue
            review_guitar(crds, obj)
