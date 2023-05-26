"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3



bucket = s3.Bucket("my-test",
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    ),
)




bucket = s3.Bucket("my-test-2",
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    ),
)

ownership_controls = s3.BucketOwnershipControls(
    'ownership-controls',
    bucket=bucket.id,
    rule=s3.BucketOwnershipControlsRuleArgs(
        object_ownership='ObjectWriter',
    ),
)

public_access_block = s3.BucketPublicAccessBlock(
    'public-access-block', bucket=bucket.id, block_public_acls=False
)

bucket_object = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('index.html'),
    content_type='text/html',
    acl='public-read',
    opts=pulumi.ResourceOptions(depends_on=[public_access_block]),
)
pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))