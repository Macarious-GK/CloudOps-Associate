resource "aws_cloudtrail" "example" {
  name                          = var.trail_object.name
  s3_bucket_name                = var.trail_object.s3_bucket_name
  s3_key_prefix                 = var.trail_object.s3_key_prefix
}


data "aws_s3_bucket" "example" {
  bucket = var.trail_object.s3_bucket_name

}


data "aws_iam_policy_document" "example" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:GetBucketAcl"]
    resources = [data.aws_s3_bucket.example.arn]
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:${data.aws_partition.current.partition}:cloudtrail:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:trail/${var.trail_object.name}"]
    }
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${data.aws_s3_bucket.example.arn}/${var.trail_object.s3_key_prefix}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:${data.aws_partition.current.partition}:cloudtrail:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:trail/${var.trail_object.name}"]
    }
  }
}

resource "aws_s3_bucket_policy" "example" {
  bucket = data.aws_s3_bucket.example.id
  policy = data.aws_iam_policy_document.example.json
}

data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

data "aws_region" "current" {}

output "aws_caller_identity" {
    value = data.aws_caller_identity.current
}
output "aws_partition" {
    value = data.aws_partition.current
}
