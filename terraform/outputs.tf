output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = module.ec2.instance_id
}

output "ec2_public_ip" {
  description = "EC2 public IP — use this to access the application"
  value       = module.ec2.public_ip
}

output "s3_bucket_name" {
  description = "S3 bucket for build artifacts"
  value       = module.ec2.s3_bucket_name
}
