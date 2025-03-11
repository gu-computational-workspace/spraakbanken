<p>To run the transformers script by submitting it as a ray job to the cluster, the oc command needs to be present. You can get the oc command here https://downloads-openshift-console.apps.op1.compute.gu.se/amd64/linux/oc.tar</p>

<p>You further need to be logged on to the cluster, in the right project and with port forwarding setup. This is only required in the test environment. When in production, a submission url will be provided. For now the following is needed:</p>

```
[root@csc01-p kuberay]# wget https://downloads-openshift-console.apps.op1.compute.gu.se/amd64/linux/oc.tar
[root@csc01-p kuberay]# tar -xvf oc.tar
[root@csc01-p kuberay]# chmod +x oc
[root@csc01-p kuberay]# mv oc /usr/bin/oc
[root@csc01-p kuberay]# oc login --server=https://api.op1.compute.gu.se:6443 -u <x-konto>
[root@csc01-p kuberay]# oc project cspace-sb
Already on project "cspace-sb" on server "https://api.op1.compute.gu.se:6443".
[root@csc01-p kuberay]# oc get pods |grep head
kuberay-cluster-head-nbkkm                             2/2     Running   0              4h57m
[root@csc01-p kuberay]# oc port-forward kuberay-cluster-head-nbkkm 8265:8265 >/dev/null 2>&1 &
[1] 14017
```
