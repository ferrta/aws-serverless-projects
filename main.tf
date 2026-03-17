# Provider - tells Terraform to use AWS
provider "aws" {
  region = "region of your choice"
}

# Resource - what you want to create
resource "aws_instance" "my_server" {
  ami           = "your ami"  
  instance_type = "t2.micro"
   key_name      = "your keypair"
  tags = {
    Name = "TerraformTest"
  }
 
}