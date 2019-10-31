import time

from app.service.resources.aggregate import AggregateResources

if __name__ == '__main__':
    user = 'mailchimp'
    start = time.time()
    resource = AggregateResources(user)
    resource.process_resources()
    print(resource.aggregate_results())
    print(resource.get_resource_errors())
    end = time.time()
    print('Time taken in seconds -', end - start)
