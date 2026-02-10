# Create IAM Policy
# There are a few ways to create an IAM Policy. You can use the (file, "jsonencode" function, a heredoc string, or the "aws_iam_policy_document") data source to generate the policy document on JSON Formate. 
# The "aws_iam_policy_document" data source is the most flexible . It also check for syntax errors.

# After we create the policy & create the users we can attach it to the user, role, or group.


# Policies
resource "aws_iam_policy" "policy_1" {
  name        = "test_policy_1_eof"
  path        = "/"
  description = "My test policy NO.1 EOF"
  
  policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:Describe*"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }
    ]
  }
    EOF
}

resource "aws_iam_policy" "policy_2" {
  name        = "test_policy_2_jsonencode"
  path        = "/"
  description = "My test policy NO.2 JSONENCODE"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:StartInstances",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_policy" "policy_3" {
  name        = "test_policy_3_file"
  path        = "/"
  description = "My test policy NO.3 file"

  policy = file("${path.module}/policy_3.json")
}

resource "aws_iam_policy" "policy_4" {
  name        = "test_policy_4_data"
  path        = "/"
  description = "My test policy NO.4 data"

  policy = data.aws_iam_policy_document.policy_4.json
}

data "aws_iam_policy_document" "policy_4" {
  statement {
    sid = "1"

    actions = [
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation",
    ]

    resources = [
      "arn:aws:s3:::*",
    ]
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy" "adminaccess" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

locals {
  policies_arn = {
    policy_1 = aws_iam_policy.policy_1.arn
    policy_2 = aws_iam_policy.policy_2.arn
    policy_3 = aws_iam_policy.policy_3.arn
    policy_4 = aws_iam_policy.policy_4.arn
    adminaccess = data.aws_iam_policy.adminaccess.arn
  }
}

# IAM Users
resource "aws_iam_user" "user" {
  name = "test-user"
  path = "/mac_user/"
  tags = {
    tag-key = "tag-test-user"
  }

}

resource "aws_iam_user_policy_attachment" "test-attach" {
    for_each = local.policies_arn
    user       = aws_iam_user.user.name
    policy_arn = each.value
}

# IAM Roles

resource "aws_iam_role" "test_role" {
  name = "test_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json

  tags = {
    tag-key = "tag-value"
  }
}

resource "aws_iam_role_policy_attachment" "test-attach" {
    for_each = local.policies_arn
    role       = aws_iam_role.test_role.name
    policy_arn = each.value
}

output "policies_arn" {
    value = local.policies_arn
}
