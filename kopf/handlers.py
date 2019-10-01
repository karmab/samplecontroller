import json
import kopf
from kubernetes import client


DOMAIN = "kool.karmalabs.local"
goodbrands = ['coleclark', 'fender', 'gibson', 'ibanez', 'martin', 'seagull', 'squier', 'washburn']
badbrands = ['epiphone', 'guild', 'gretsch', 'jackson', 'ovation', 'prs', 'rickenbauer', 'taylor', 'yamaha']


def review_guitar(name, namespace):
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    crds = client.CustomObjectsApi(api_client)
    guitar = crds.get_namespaced_custom_object(DOMAIN, 'v1', namespace, 'guitars', name)
    metadata = guitar.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(guitar, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    guitar["spec"]["review"] = True
    brand = guitar["spec"]["brand"]
    if brand in goodbrands:
        guitar["spec"]["comment"] = "this is a great instrument"
    elif brand in badbrands:
        guitar["spec"]["comment"] = "this is shit"
    else:
        guitar["spec"]["comment"] = "nobody knows this brand"
    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "guitars", name, guitar)


@kopf.on.create('kool.karmalabs.local', 'v1', 'guitars')
# def create_fn(body, **kwargs):
def create_fn(meta, spec, namespace, logger, **kwargs):
    name = meta.get('name')
    print("Handling %s" % (name))
    done = spec.get("review", False)
    if done:
        return
    else:
        review_guitar(name, namespace)
