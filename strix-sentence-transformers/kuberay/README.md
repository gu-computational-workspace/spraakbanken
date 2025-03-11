To run the transformers script by submitting it as a ray job to the cluster, the oc command needs to be present. You can get the oc command here https://downloads-openshift-console.apps.op1.compute.gu.se/amd64/linux/oc.tar

You further need to be logged on to the cluster, in the right kubernetes namespace (project) and with port forwarding setup. This is only required in the test environment. When in production, only the job submission url needs to be specified. For now the following is needed:

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
Runtime environments are used for application dependencies. Dependencies are installed dynamically on the cluster at runtime and cached for future use. In this example we specify the runtime environment on a per job basis. We do so in the run_ray_transformers.py file. Any packages specified in the requirements.txt file will be installed. Also note that we have set the working directory to `./`. This means that any files in this directory will be uploaded to the cluster at runtime and accessible from the application code. You can read more about environment dependencies [here](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html)

The only python function in the application code that is specified as a Ray remote function is `def main(corpius)`. That is because that is where the grunt takes place. Such functions are executed asynchronically on separate worker nodes and, when invoced, are called [Ray tasks](https://docs.ray.io/en/latest/ray-core/tasks.html). By decorating the python function with `@ray.remote(num_gpus=1)` it becomes a Ray remote function. Note that we specify a task resource requirement, namely `num_gpus=1`.
