To run the Transformers script by submitting it as a Ray job to the cluster, the oc command must be available. You can download it here: [OpenShift CLI (oc) download.](https://downloads-openshift-console.apps.op1.compute.gu.se/amd64/linux/oc.tar)

Additionally, you need to be logged into the cluster in the correct Kubernetes namespace (project) and have port forwarding set up. This is only required in the test environment. In production, only the job submission URL needs to be specified.

For now, the following is required:

```
[root@csc01-p kuberay]# wget https://downloads-openshift-console.apps.op1.compute.gu.se/amd64/linux/oc.tar
[root@csc01-p kuberay]# tar -xvf oc.tar
[root@csc01-p kuberay]# chmod +x oc
[root@csc01-p kuberay]# mv oc /usr/bin/oc
[root@csc01-p kuberay]# oc login --server=https://api.op1.compute.gu.se:6443 -u <x-konto>
[root@csc01-p kuberay]# oc project cspace-sb
Already on project "cspace-sb" on server "https://api.op1.compute.gu.se:6443".
[root@csc01-p kuberay]# oc get pods |grep head
kuberay-cluster-head-ngqhf                             2/2     Running   0              4h57m
[root@csc01-p kuberay]# oc port-forward kuberay-cluster-head-ngqhf 8265:8265 >/dev/null 2>&1 &
[1] 14017
```
Runtime environments are used to manage application dependencies. Dependencies are dynamically installed on the cluster at runtime and cached for future use, eliminating the need to build or maintain custom container images.

In this example, we specify the runtime environment on a per-job basis in the `run_ray_transformers.py` file. Any packages listed in the `requirements.txt` file will be installed. Additionally, we have set the working directory to `./`, meaning that all files in this directory will be uploaded to the cluster at runtime and will be accessible from the application code. You can read more about environment dependencies [here](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html)

Note that working directories can be specified as [remote URIs](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html#remote-uris), such as a S3 bucket. I strongly recommend considering the use of object storage buckets instead of local or network storage wherever appropriate.

Spraakbanken aims to run arbitrary Python code or applications in the cluster with minimal modifications. For this reason, none of the functions have been marked as Ray remote functions, meaning we are not leveraging Ray's parallel or distributed execution paradigm. This will be evident when viewing the Jobs in the [Ray Dashboard](https://ray-dashboard-kuberay-cluster-cspace-sb.apps.op1.compute.gu.se), where it will indicate that "no Ray driver" was present. 

However, if we wanted to take advantage of this capability, we could define the function `def main(corpius)` as a Ray remote function. Such functions execute asynchronously on separate worker nodes and, when invoked, are referred to as [Ray tasks](https://docs.ray.io/en/latest/ray-core/tasks.html). By decorating the Python function with `@ray.remote(num_gpus=1)`, it becomes a Ray remote function. However, for now, we keep it simple by running the application code on a single worker node with access to a single GPU instance.

In production, we may want to revisit this approach and consider using multiple GPU instances per worker.

The sbdata01 network share is mounted in the worker nodes. The mount point is `/mnt/sbdata01`. The transformers data directory is set to `transformers_postprocess_dir: /mnt/sbdata01/strix/kuberay/transformers_data` in the `config.yml` file. 

To submit the Ray job, or python application, run the following:
```
python run_ray_transformers.py <corpus>
```
Test data is present for 'jubileumsarkivet-pilot', 'wikipedia-sv', 'kalmar-newspaper-ocr' and 'kalmar-newspaper-original'.

Eaxample job submission:
```
[root@csc01-p kuberay]# python run_ray_transformers.py wikipedia-sv
2025-03-12 21:47:58,173	INFO dashboard_sdk.py:338 -- Uploading package gcs://_ray_pkg_981c598ce02b8e44.zip.
2025-03-12 21:47:58,174	INFO packaging.py:575 -- Creating a file package for local module './'.
raysubmit_5n9g5RZ1dRPaa1AE
```
You can login to the [Ray Dashboard](https://ray-dashboard-kuberay-cluster-cspace-sb.apps.op1.compute.gu.se) with your xkonto credentials to monitor jobs. You can also programatically control and monitor running jobs.

I will update the code to use object buckets instead of local or network storage. This approach is simple to implement, enhances portability, and eliminates the need for network storage, which is not an elegant solution in frameworks like Ray.
