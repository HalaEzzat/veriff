# Veriff DevOps (Observability) Engineer Task
---------------------------------------------
## Task
1. Create a Kubernetes Cluster:
- Use any technology of your preference (e.g., Minikube, Kind, K3s, EKS,
GKE, AKS, etc.).
- Ensure the cluster is configured to support deployments and
observability tooling.

2. Deploy a Telemetry Collection Stack:
- Choose an observability stack (e.g., ELK, LGTM, OpenTelemetry,
Prometheus + Grafana, etc.).
- Ensure the stack collects and stores logs, metrics, and traces.

3. Deploy an Application:
- Deploy any application of your choice (e.g., a simple web app, an
API service, etc.).
- The application should have observable telemetry (logs, metrics,
traces).

4. Monitor the Service:
- Implement monitoring for the deployed application.
- Demonstrate the ability to identify key metrics and set up at least
one alert based on observed telemetry.

----------------------------------------------------------------
## Solution 

I tried multiple approches to solve the challenge .
One of them I tried LGTM stack.

I decided to go with Promethues+Grafana + Datadog , because it provided the easiest to install , integrate and demo.

My solution: 
- Used Terraform to provession EKS Cluster [No security applied for easier Deployment and Kubectl, Not production environment]
- Demo App: is from this repo : https://github.com/DataDog/ecommerce-workshop [it provides the perfect app for observability with issues]
- Deploy app to EKS using Github Actions
- Deploy promethues + grafana to EKS using Helm
- Deploy Datadog to EKS using Helm
------------------------------------------------------------------
## Steps to run the solution:

1- create s3 bucket for state file and github actions using command:
```sh
aws s3api create-bucket --bucket veriff-terraform-state-bucket --region us-east-1 
```
2- Create AWS key and Datadog free account using your Google account and then create API and APP keys 
3- Add your secrets to github actions replacing `AWS_ACCESS_KEY_ID` , `AWS_REGION`, `AWS_SECRET_ACCESS_KEY`, `DATADOG_API_KEY` , `DATADOG_APP_KEY`
4- Click on the `Actions` tab then choose our CICD pipeline: `Manage EKS Infrastructure` from the side menue . then choose `deply` from the drop down menue.
5- Check the cluster for all pods to be `running`
6- Run the following command to access our app:
```sh
kubectl get svc frontend
```
7- Run the following command to access grafana:
```sh
kubectl get svc grafana
```
Username*: `admin`
Password*: `supersecurepassword`
8- Add Promethues as a Datasource:
URL*: `http://prom-kube-prometheus-stack-prometheus:9090`
- Import Prometheus Dashboards
- Go to Dashboards > Manage.
- Click Import.
- Enter the following dashboard IDs (one at a time):
- Kubernetes / Node: `1860`
- Kubernetes / Pods: `6417`
- Kubernetes / Deployment: `3131`
- Select the `Prometheus` data source for each dashboard.
- Click `Import`.
-----------------------------------------------
## Results:

### Promethues + Grafana:

APM (This is my app):
![image](https://github.com/user-attachments/assets/65d5e84d-f3f8-4070-ab81-dd6ad938a7d0)

K8s (Demo App) :
![image](https://github.com/user-attachments/assets/88a082f7-31d0-4939-99e2-98fa45a87ba0)
![image](https://github.com/user-attachments/assets/87b009a2-5bf8-41ef-8623-dcc49d50b065)
![image](https://github.com/user-attachments/assets/0a513df4-a99d-4c3a-8fda-14412d1fab98)

Datadog (Demo App):

APM:

![python dashboard](https://github.com/user-attachments/assets/e6b32d52-0f8e-43fe-b6a0-7b47c57079c1)
![apm agent](https://github.com/user-attachments/assets/22f38d03-f6a7-43bb-b0db-4ea54950986e)
![apm services configured](https://github.com/user-attachments/assets/2bd268d3-da88-4513-9158-f02e5ee870d7)
![apm traces](https://github.com/user-attachments/assets/1ce0df14-1115-4e17-aa39-4181bf4c52b6)
![service traces](https://github.com/user-attachments/assets/48c89431-ca86-403a-9bde-5f5d0b408ea0)
![image](https://github.com/user-attachments/assets/fca095ef-193c-4652-b4d3-9dc4e182c126)



K8s:

![cluster dashboard](https://github.com/user-attachments/assets/6866229d-13aa-44f7-a1a0-1a1e71e21248)
![k8s cluster cpu and memory](https://github.com/user-attachments/assets/b626984d-82ba-4ba9-b4e2-f44ca9b72b7d)
![k8s cluster dashboard](https://github.com/user-attachments/assets/9812cf30-dfab-48ee-9219-204674dcd913)

Logs:

![logs dashboard](https://github.com/user-attachments/assets/ecd2f508-84d9-4241-b5bc-4cf7523345bc)

Monitors and Alerts:

![image](https://github.com/user-attachments/assets/d2a2f27e-7a0c-4f32-ac6f-1cd7847008b0)
![image](https://github.com/user-attachments/assets/5cbbe00b-1db8-404d-9293-1aa880c3d70a)














  

 
