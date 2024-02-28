
## Input customer Requirement
- Customer will provide a spec.json file in the `input` directory.
- A sample is provided.
- The key value names in the file are self explanatory.

spec.json sample is also shown below:
```
{
    "targetManagedClusters": 100,
    "numberOfPoliciesPerCluster": 5,
    "numberOfAppsPerCluster": 1500,
    "numberOfTimeSeriesPerCluster": 25000,
    "numberOfResourcesPerCluster": 10000
}
```
## To run the program

1. Clone this repo
1. Setup venv
    - `cd to the repo dir`
    - run: 
        ```
        python -m venv .venv
        source .venv/bin/activate
        pip install -r src/requirements.txt
        ```
    - run :`which python` and this show that python is being used from the venv directory
1. Run the program
    - then to run the program, just run 
        ```
        cd src
        python main.py
        ```
1. After all work is done, to exit the venv, just run: `deactivate`


## Developer notes

### Understand the metrics

|Metric name|Meaning|Calculation
|---|---|---|
|cluster-count|---|max(apiserver_storage_objects{resource=~"managedclusters.cluster.open-cluster-management.io"})|
|---|---|---|
|etcdetcdDBSizeMB|the units are in KB and not MB!|query='sum(etcd_mvcc_db_total_size_in_bytes{job="etcd"})/(1024*1024)'|
|---|---|---|
|KubeAPIMemUsageWSSGB|accounts for kube api and etcd|query='sum(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!="",namespace=~"openshift-kube-apiserver|openshift-etcd"})/(1024*1024*1024)'|
|OtherMemUsageWSSGB|excludes kube api, etcd and all ACM namespaces |query='sum(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!="",namespace!~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"})/(1024*1024*1024)'|
|ACMObsMemUsageWSSGB	|contains usage of all ACM Obs pods (except for metric collector - which is minimal)|query='sum(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!="",namespace="open-cluster-management-observability"})/(1024*1024*1024)'|
|ACMOthMemUsageWSSGB|all ACM except observability **|query='sum(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", image!="",namespace=~"multicluster-engine|open-cluster-management-agent.+|open-cluster-management-hub|open-cluster-management-addon.+"})/(1024*1024*1024)'|
|ClusterMemUsageGB|Overall usage at a cluster level|query='(sum(node_memory_MemTotal_bytes{job="node-exporter",cluster=""}) -sum(:node_memory_MemAvailable_bytes:sum{cluster=""}) )/(1024*1024*1024)'|
|---|---|---|
|KubeAPICPUCoreUsage|accounts for kube api and etcd|query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"openshift-kube-apiserver|openshift-etcd"})'|
|OtherCPUCoreUsage|excludes kube api, etcd and all ACM namespaces|query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace!~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"}'|
|---|---|---|
|ACMObsCPUCoreUsage|contains usage of all ACM Obs pods|query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace="open-cluster-management-observability"})'|
|ACMOthCPUCoreUsage|all ACM except observability **|query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-management-agent.+|open-cluster-management-hub|open-cluster-management-addon.+"})'|
|ClusterCPUCoreUsage|Overall usage at a cluster level|query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate)'|
|ClusterCPUUsage	|Overall usage at a cluster level|same as ClusterCPUCoreUsag |
|---|---|---|
|TimeSeriesCount|Total time series being ingested at Thanos receiever|query='sum(acm_prometheus_tsdb_head_series)/3'|


### Missing
- Search consumption needs to be separate
- Consumption of open-cluster-management ns is missing

