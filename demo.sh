#!/bin/bash

source `which util.sh`
HOST="192.168.122.225"
USER="developer"
PASSWORD="developer"
PROJECT="guitarcenter"

backtotop
desc "Login in our project"
run "oc login --insecure-skip-tls-verify=true -u $USER -p $PASSWORD https://$HOST:8443"

backtotop
desc "Create a project and give enough permissions to default service account"
run "oc new-project guitarcenter"
run "oc adm policy add-cluster-role-to-user cluster-admin -z default -n $PROJECT"

backtotop
desc "Deploy our custom controller"
run "oc new-app karmab/samplecontroller"

backtotop
desc "See how custom resource definition has been created for us"
run "oc get crd"

backtotop
desc "Create some guitars and see the results"
run "oc create -f crd/stratocaster.yml"
run "oc create -f crd/lespaul.yml"
run "oc get guitars -o yaml"

backtotop
desc "Use additional UI to do the same"
run "oc new-app karmab/sampleui"
run "oc expose svc sampleui"
run "oc get route"

backtotop
desc "Clean things up"
run "oc project default"
run "oc delete project $PROJECT"
