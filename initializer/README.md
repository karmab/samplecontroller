

This demonstrates how to run a basic [initializer](https://kubernetes.io/docs/admin/extensible-admission-controllers) with python kubernetes library 
the sample code allows to injects a given image in all your deployments (or filter with a specific annotation)

## requisites

a cluster with --admission-control:

```
minikube start --extra-config=apiserver.Admission.PluginNames="Initializers,NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota"
```


# launch the initializer controller
you can use the two following optional environment variables:

- *INJECT_POD*  pointing to the image to inject in the deployment containers list
- *ANNOTATION*  the name of an annotation to restricts pod injection only to deployments having the corresponding annotation set to "true"

You can then either manually launch the controller

```
python initializer.py
```

Or run it as a deployment ( note that we prevent the controller to be affected by any existing initializer )

```
kubectl create -f initializer.yml
```


On openshift 

```
oc new-project initializer
oc adm policy add-cluster-role-to-user cluster-admin -z default -n initializer
oc new-app karmab/sampleinitializer
```

## define which elements get initialized

this snippet with create an initialization configuration matching deployments

```
kubectl create -f initialization_deployments.yml
```


test with with a sample deployment 

```
kubectl run nginx --image=nginx
kubectl describe deployment nginx
```

# TO DO

- use go instead of python
- autocreate the initializer configuration when starting the controller
- store this conf in a configmap and read it when starting

## based on [keylsey hightower initializer tutorial](https://github.com/kelseyhightower/kubernetes-initializer-tutorial)
