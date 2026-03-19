# devops-ci-cd-demo

A production-style DevOps project demonstrating a full CI/CD pipeline — from code commit to Kubernetes deployment — using Jenkins, GitHub Actions, Docker, Terraform, and AWS.

---

## Architecture

```
Developer Push
      │
      ▼
┌─────────────────────────────────────────────┐
│           CI/CD Pipeline                    │
│                                             │
│  GitHub Actions  ──OR──  Jenkins            │
│                                             │
│  1. Checkout code                           │
│  2. Run pytest unit tests                   │
│  3. Build Docker image                      │
│  4. Push to DockerHub                       │
│  5. Update K8s deployment manifest          │
│  6. kubectl apply → Kubernetes cluster      │
│  7. Verify rollout + health checks          │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│         AWS Infrastructure (Terraform)      │
│                                             │
│  VPC (10.0.0.0/16)                         │
│  ├── Public Subnet ap-south-1a             │
│  ├── Public Subnet ap-south-1b             │
│  ├── Internet Gateway                       │
│  ├── EC2 t3.micro (app server)             │
│  └── S3 Bucket (build artifacts)           │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│         Kubernetes Cluster                  │
│                                             │
│  Namespace: devops-demo                     │
│  ├── Deployment (2 replicas)               │
│  │   ├── Liveness probe  → /health         │
│  │   └── Readiness probe → /ready          │
│  └── Service (ClusterIP → port 80)         │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│         Flask Application                   │
│                                             │
│  GET /        → app status + version        │
│  GET /health  → liveness check              │
│  GET /ready   → readiness check             │
└─────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer              | Tool/Service                          |
|--------------------|---------------------------------------|
| Application        | Python 3.11, Flask                    |
| Containerisation   | Docker (multi-stage build)            |
| Orchestration      | Kubernetes, kubectl                   |
| CI/CD              | Jenkins (Jenkinsfile), GitHub Actions |
| Infrastructure     | Terraform (modular — VPC, EC2, S3)    |
| Cloud              | AWS (EC2, S3, VPC, IAM)               |
| Registry           | DockerHub                             |
| Testing            | pytest, pytest-flask                  |

---

## Project Structure

```
devops-ci-cd-demo/
├── app/
│   ├── app.py                   # Flask application
│   ├── requirements.txt
│   └── tests/
│       └── test_app.py          # Unit tests (pytest)
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml          # 2 replicas, liveness + readiness probes
│   └── service.yaml
├── terraform/
│   ├── main.tf                  # Root module — calls vpc + ec2 modules
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── vpc/                 # VPC, subnets, IGW, route tables
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       └── ec2/                 # EC2 instance, security group, S3 bucket
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # GitHub Actions pipeline
├── Jenkinsfile                  # Jenkins pipeline
├── Dockerfile                   # Multi-stage Docker build
└── .gitignore
```

---

## CI/CD Pipeline Flow

### GitHub Actions (`.github/workflows/ci-cd.yml`)

Triggers on push or PR to `main` branch:

```
test job
  └── checkout → install dependencies → pytest

build-and-push job  (main branch only, after test passes)
  └── docker login → build image → push :latest + :run_number

deploy job  (main branch only, after build-and-push)
  └── configure kubectl → update image tag in manifest
      → kubectl apply → rollout status → verify pods
```

### Jenkins (`Jenkinsfile`)

Same stages, designed for self-hosted Jenkins with DockerHub credentials configured.

---

## Infrastructure (Terraform)

**VPC Module** (`terraform/modules/vpc/`)
- VPC with DNS support enabled
- 2 public subnets across availability zones
- Internet Gateway + route table associations

**EC2 Module** (`terraform/modules/ec2/`)
- t3.micro EC2 instance (Ubuntu 22.04)
- Security group — HTTP (80), app port (5000), SSH (22)
- S3 bucket with versioning enabled for build artifacts

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

## Local Setup

**Run with Docker**
```bash
docker build -t devops-ci-cd-demo .
docker run -p 5000:5000 devops-ci-cd-demo
# Visit http://localhost:5000
```

**Run tests**
```bash
pip install -r app/requirements.txt
pytest app/tests/ -v
```

**Deploy to Kubernetes**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -n devops-demo
```

---

## Key Concepts Demonstrated

- **Multi-stage Docker build** — separates build and runtime stages to reduce final image size
- **Kubernetes health probes** — liveness and readiness endpoints ensure zero-downtime rolling updates
- **Reusable Terraform modules** — VPC and EC2 modules are independently reusable across environments
- **Dual CI/CD pipelines** — same workflow implemented in both Jenkins and GitHub Actions
- **Environment separation** — namespace isolation in Kubernetes; environment tags on all AWS resources

---

## GitHub Actions Secrets Required

| Secret               | Description                    |
|----------------------|--------------------------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username        |
| `DOCKERHUB_TOKEN`    | DockerHub access token         |
| `KUBECONFIG`         | Base64-encoded kubeconfig file |

---

## Author

**Rajkumar Asam** — Software Engineer (DevOps)
[linkedin.com/in/rajkumarasam17](https://linkedin.com/in/rajkumarasam17) | [github.com/Rajkumarasam](https://github.com/Rajkumarasam)
