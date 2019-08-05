# Overview

This folder provides a set of utilities for deploying the **Cloud Innovation Platform** on **Amazon Web
Service infrastructure**.

TODO: add image



# What gets created

To be documented



## Network helpers

To be documented



### Remote admin bastions

To be documented



### VPN Concentrators

To be documented



### Proxy / NAT Instances

Legal filtering (warez, terrorism, etc.) is mandatory, as well as tracing all browsing activities.
This is accomplished with custom NAT instances using Squid.

All outgoing network traffic, including traffic coming from network appliances such as WAF, VPN concentrators and the NAT instances themselves is traced in the Squid logs.

Some wellknown URLs have been excluded thaugh to avoid tracing the same activity in various log concentrators and reduce disk space.

The filtered URLs are:

| URL                                 | Explanations                   |
|-------------------------------------|--------------------------------|
| log.{{region}}.amazonaws.com        | CloudWatch Logs agents traffic |
| monitoring.{{region}}.amazonaws.com | CloudWatch Metrics traffic     |
| localhost                           | Squid cache metrics gathering, filter could be improved. |



### Reverse Proxy / WAF Instances

To be documented



## Network addressing

Planning a network addressing plan is not that easy as many parameters need to be taken into account
to make sure your design will scale and allow future use case.

The following segmentation would fit most needs.

| VPC             | CIDR          | # IPs  | Subnet   | Comments |
|-----------------|--------------:|-------:|----------|----------|
| CIAP (Hosting)  | 10.0.0.0/20   | 4094   | supernet | 1 subnet per AZ, max 1022 IP/AZ, seems enough |
| Admin           | 10.0.16.0/20  | 4094   | supernet | 1 subnet per AZ, max 1022 IP/AZ, seems enough |
| Tech            | 10.0.32.0/20  | 4094   | supernet | 1 subnet per AZ, max 1022 IP/AZ, seems enough |
| CIAP (Browsing) | 10.0.48.0/20  | 4094   | supernet | 1 subnet per AZ, max 1022 IP/AZ, seems enough |
| Project         | 10.0.128.0/17 | 32766  | supernet | Many subnets for various usage, aPaaS, CaaS, EC2 instances, etc. |
| Project         | 10.0.128.0/24 | 254    | OpenShift Pub 1 | Public Subnet for OpenShift in AZ 1 |
| Project         | 10.0.129.0/24 | 254    | OpenShift Pub 2 | Public Subnet for OpenShift in AZ 2 |
| Project         | 10.0.130.0/24 | 254    | OpenShift Pub 3 | Public Subnet for OpenShift in AZ 3 |
| Project         | 10.0.131.0/24 | 254    | OpenShift Pub 4 | Reserving for Public Subnet for OpenShift in AZ 4 |
| Project         | 10.0.132.0/24 | 254    | OpenShift Priv 1 | Private Subnet for OpenShift in AZ 1 |
| Project         | 10.0.133.0/24 | 254    | OpenShift Priv 2 | Private Subnet for OpenShift in AZ 2 |
| Project         | 10.0.134.0/24 | 254    | OpenShift Priv 3 | Private Subnet for OpenShift in AZ 3 |
| Project         | 10.0.135.0/24 | 254    | OpenShift Priv 4 | Reserving for Private Subnet for OpenShift in AZ 4 |

At time of writing, VPC CIDR on AWS are limited to /16 (65534 IP addresses).



## Project - Red Hat Openshift Container Platform

- Multi-master / Multi-AZs deployment [based on this article](https://access.redhat.com/documentation/en-us/reference_architectures/2018/html/deploying_and_managing_openshift_3.9_on_amazon_web_services/index). The doc is related to OpenShift 3.9 but the code in this repository will deploy the latest OpenShift 3.xx version. At time of writing, the latest version is OpenShift 3.11



# Deploying the platform

Work in progress, but the following should help you getting started.

1. Fork the repository, if not done already and clone it on your workstation.

2. Copy the ansible variable sample file and adapt to your environment

```
$ cp playbooks/vars/main.yaml.sample playbooks/vars/main.yaml
```

3. Browse the roles template files and adapt if needed

4. Run the cip-on-aws.py utility to prepare the AWS environment.

   If you don't specify the required parameters on the command line, you'll be prompted.
   Here is an example to run it with the mandatory ones:

```
$ ./cip-on-aws.py -v --task=launch --stack-name=cip-dev \
                     --public-dns-domain=cip-dev.domain.com \
                     --private-dns-domain=cip-dev.domain.priv \
                     --keypair=aws-key-pair-name
```

5. Trigger the OpenShift admin, master, infra and worker nodes creation

```
$ ansible-playbook -vvv -i inventory/aws/hosts \
    -e 'stack_name=cip-dev keypair=aws-key-pair-name cluster_id=my' \
    -e 'public_dns_domain=cip-dev.domain.com private_dns_domain=cip-dev.domain.priv' \
    playbooks/ocp_cluster.yaml
```

6. Log on the openshift administration node created at step 4 and trigger the OpenShift installation

To be documented

# Deploying the platform in AWS China regions

## Route53

As of writing, this service is still in beta so you must be enrolled first.

You also need to patch botocore since the route53 service is not defined yet in the AWS China partition.

```shell
# diff botocore/data/endpoints.json botocore/data/endpoints.json.orig
--- botocore/data/endpoints.json
+++ botocore/data/endpoints.json.orig
@@ -3357,19 +3357,6 @@
           "cn-northwest-1" : { }
         }
       },
-      "route53" : {
-        "endpoints" : {
-          "aws-cn-global" : {
-            "credentialScope" : {
-              "region" : "cn-northwest-1"
-            },
-            "hostname" : "api.route53.cn",
-            "protocols" : [ "http", "https" ]
-          }
-        },
-        "isRegionalized" : false,
-        "partitionEndpoint" : "aws-cn-global"
-      },
       "cloudfront" : {
         "endpoints" : {
           "aws-cn-global" : {

```

# Troubleshooting

To be documented



### Verifying if a master is up

#### From a master node

Run the following command:

```
curl --silent --tlsv1.2 --cacert /etc/origin/master/ca-bundle.crt https://internal-openshift-master.{{public_dns_domain}}/healthz/ready
```
