provider "aws" {
  region = "us-east-1"
}


resource "aws_s3_bucket_versioning" "versioning" {
  bucket  = "veriff-terraform-state-bucket"
  versioning_configuration {
    status = "Enabled"
  }
}

terraform {
  backend "s3" {
    bucket  = "veriff-terraform-state-bucket"
    key     = "terraform/state.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

# 🚀 VPC for EKS
resource "aws_vpc" "eks_vpc" {
  cidr_block = "10.0.0.0/16"
}

# 🌍 Public Subnet 1
resource "aws_subnet" "eks_subnet_1" {
  vpc_id                  = aws_vpc.eks_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

# 🌍 Public Subnet 2
resource "aws_subnet" "eks_subnet_2" {
  vpc_id                  = aws_vpc.eks_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}

# 🔹 IAM Role for EKS
resource "aws_iam_role" "eks_role" {
  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = [
            "eks.amazonaws.com",
            "ec2.amazonaws.com"
          ]
        }
      }
    ]
  })
}

# 🌟 Attach Necessary Policies
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_role.name
}

resource "aws_iam_role_policy_attachment" "eks_service_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.eks_role.name
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_role.name
}

resource "aws_iam_role_policy_attachment" "ec2_container_registry_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_role.name
}

# 🎯 Create EKS Cluster
resource "aws_eks_cluster" "eks" {
  name     = "veriff-cluster"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.eks_subnet_1.id,
      aws_subnet.eks_subnet_2.id
    ]
  }
}

# 🚀 Node Group for EKS (Optimized for Fast Deployment)
resource "aws_eks_node_group" "eks_nodes" {
  cluster_name  = aws_eks_cluster.eks.name
  node_role_arn = aws_iam_role.eks_role.arn
  subnet_ids    = [
    aws_subnet.eks_subnet_1.id,
    aws_subnet.eks_subnet_2.id
  ]

  # ✅ Using Smallest Instance Type for Quick Deployment
  instance_types = ["t3.small"]

  # ✅ Minimal Nodes to Reduce Cost & Speed Up Deployment
  scaling_config {
    desired_size = 1
    max_size     = 2
    min_size     = 1
  }
}
