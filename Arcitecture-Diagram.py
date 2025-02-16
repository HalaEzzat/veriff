from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.security import IAMRole
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.config import Ansible
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus, Grafana, Loki
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV

with Diagram("EKS Architecture with CI/CD, Flask App, and Monitoring", show=False):
    
    github = GithubActions("GitHub Actions")
    ansible = Ansible("Ansible")
    docker = Docker("Docker")
    
    with Cluster("AWS Infrastructure"):
        vpc = VPC("VPC")
        s3 = S3("Terraform State")
        iam_role = IAMRole("EKS IAM Role")
        
        with Cluster("EKS Cluster"):
            eks = EKS("EKS Control Plane")
            
            with Cluster("Worker Nodes"):
                node_group = [EC2("Node 1"), EC2("Node 2")]
                
                with Cluster("Kubernetes Resources"):
                    flask_app = Pod("Flask App")
                    service = Service("Service")
                    pvc = PV("Persistent Volume")
    
    with Cluster("Monitoring Stack"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")
    
    # CI/CD Pipeline
    github >> Edge(label="Build & Push") >> docker
    docker >> Edge(label="Deploy with") >> ansible
    ansible >> Edge(label="Provision") >> eks
    eks >> Edge(label="Deploy Pods") >> flask_app
    
    # Networking & Monitoring
    flask_app >> Edge(label="Handles Requests") >> service
    flask_app >> Edge(label="Logs & Metrics") >> [prometheus, grafana, loki]
    service >> Edge(label="Uses Storage") >> pvc
