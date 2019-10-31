from app.service.resources.resources import GitHubResource, BitBucketResource

# This defines the resource classes to be used in AggregateResource. It must be of dict type
# The key is the name of the instance to be created and the value
# must be a subclass of Resource from app.service.resources and implement all the abstract methods of the Resource

resources_classes = {'github': GitHubResource, 'bitbucket': BitBucketResource}
