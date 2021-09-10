meraki

oc project meraki-events
oc new-build https://github.com/itohdai/merakiapi
oc get is

oc delete secret meraki-mongo-secret
oc create -f secret.yaml
