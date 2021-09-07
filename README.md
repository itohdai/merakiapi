meraki

oc project meraki-events
oc new-build https://github.com/itohdai/merakiapi
oc get is

oc create secret.yaml



kind: CronJob
apiVersion: batch/v1beta1
metadata:
  name: merakiapicronjob
  namespace: meraki-event
spec:
  schedule: '*/15 * * * *'
  startingDeadlineSeconds: 60
  concurrencyPolicy: Allow
  suspend: false
  jobTemplate:
    metadata:
      creationTimestamp: null
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
            - name: merakiapictn
              image: >-
                image-registry.openshift-image-registry.svc:5000/meraki-events/merakiapi
              args:
                - python
                - /usr/src/app/app.py
              env:
                - name: DATABASE_SERVICE_NAME
                  value: mongodb
                - name: MONGODB_USER
                  valueFrom:
                    secretKeyRef:
                      name: meraki-mongo-secret
                      key: database-user
                - name: MONGODB_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: meraki-mongo-secret
                      key: database-password
                - name: MONGODB_DATABASE
                  value: merakidb
                - name: MONGODB_ADMIN_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: meraki-mongo-secret
                      key: database-admin-password
              resources: {}
              terminationMessagePath: /dev/termination-log
              terminationMessagePolicy: File
              imagePullPolicy: Always
          restartPolicy: OnFailure
          terminationGracePeriodSeconds: 30
          dnsPolicy: ClusterFirst
          securityContext: {}
          schedulerName: default-scheduler
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1

apiVersion: v1
kind: Secret
metadata:
  name: meraki-mongo-secret
  namespace: meraki-event
type: Opaque 
data: 
  database-password: dmFsdWUtMg0KDQo=
  database-admin-password: dmFsdWUtMQ0K
stringData: 
  database-user: user01 
