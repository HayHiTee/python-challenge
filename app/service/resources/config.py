from app.service.resources.resources import GitHubResource, BitBucketResource

# This lists the resource classes to be used in AggregateResource
# It must be a subclass of Resource and implement all the abstract methods

resources_classes = {'github': GitHubResource, 'bitbucket': BitBucketResource}
