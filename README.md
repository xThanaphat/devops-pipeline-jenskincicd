# DevOps CI/CD Pipeline: GCP, Jenkins, Docker, Kubernetes

## Overview
This project demonstrates a full DevOps pipeline, from cloud infrastructure setup to continuous deployment using Google Cloud Platform (GCP), Jenkins, Docker, and Kubernetes. The workflow is designed to be hands-on and can be deployed on any cloud VM or lab.

---

## Workflow Steps

1. **Provision Infrastructure**  
   - Create VPC, Firewall, and Virtual Machines (VMs) on Google Cloud Platform.
2. **Setup Proxy/Networking**  
   - Install and configure HAProxy and Squid Proxy for network and security control.
3. **Install GitLab**  
   - Self-host source code and Git-based workflows.
4. **Install Docker**  
   - Build and run container images for your application.
5. **Setup Jenkins**  
   - Automated CI/CD pipeline triggered by code changes in GitLab.
6. **Deploy Kubernetes (K8s)**  
   - Run a Kubernetes cluster for application orchestration (GKE or self-managed).
7. **CI/CD Pipeline**  
   - Jenkins builds, tests, pushes Docker images, and deploys to Kubernetes.
8. **(Optional) Monitoring & Management**  
   - Use Kubernetes Dashboard, Ingress, and Helm for advanced deployment management.

---

## Key Install Commands (for Linux/Ubuntu)

### Google Cloud VM & Firewall
- Create VM and VPC using GCP Console or `gcloud` CLI.
- Configure firewall rules for Jenkins, Docker, K8s, etc.

### Proxy (HAProxy & Squid)
```bash
sudo apt update && sudo apt install -y haproxy squid
sudo systemctl enable --now haproxy
sudo systemctl enable --now squid
```

### GITLAB
```bash
sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl postfix
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
EXTERNAL_URL="http://<gitlab_ip>" sudo apt-get install gitlab-ee
```

### Docker
```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker
docker run hello-world
```

### Jenkins
```bash
sudo apt update
sudo apt install -y openjdk-11-jre
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install -y jenkins
sudo systemctl enable jenkins --now
```

### Kubernetes & Helm
```bash
sudo apt-get update
sudo apt-get install -y containerd.io kubelet=1.26.0-00 kubeadm=1.26.0-00 kubectl=1.26.0-00
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh && ./get_helm.sh

```

## End-to-End Flow

1. **Code Push: Developer pushes code to GitLab.**  
2. **CI/CD Trigger: Jenkins detects code change, builds and tests Docker image.**  
3. **Push Image: Jenkins pushes image to Docker Hub or Google Container Registry.**  
4. **K8s Deploy: Jenkins updates the deployment in Kubernetes with the new image.**  
5. **Service Live: Application is accessible via LoadBalancer IP from GCP.**  
