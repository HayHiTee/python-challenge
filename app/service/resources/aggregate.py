from app.service import AsyncRequest
from app.service.resources import config, Resource


class AggregateResources:
    """
    This resource class uses the config resource_classes to dynamically create instances of common base resource class
    and aggregate them
    :arg user: The user of the resource
    :type user: str
    :param config_resources: A list of all the resource classes that will be aggregated -> default is set resources
    classes defined in app.service.resources.config,
    :type config_resources: dict
    :ivar urls: This is used to get the urls of all the resources in order to call asynchronous requests
    :type urls: list
    :ivar _resource_instances: This stores all the instances of the resources
    :type _resource_instances: list
    """

    def __init__(self, user, config_resources=config.resources_classes):
        repo_name = 'public_repo'
        self.urls = []
        self._resource_instances = []
        self._resource_classes = config_resources
        for res in self._resource_classes.keys():
            assert issubclass(self._resource_classes[res], Resource)
            setattr(self, res, self._resource_classes[res](user))
            self.urls.append(getattr(self, res).get_repo_url(repo_name))
            self._resource_instances.append(getattr(self, res))
        print(self.urls)
        print(self._resource_instances)

    def process_resources(self):
        """ This method processes the resource by using async_request instance to process the requests of the urls
        asynchronously and latter use the setter response of each instance to get the response.
        :return:
        """
        async_request = AsyncRequest(self.urls)
        responses = async_request.run()
        for i in range(len(self._resource_instances)):
            self._resource_instances[i].response = responses[i]
            self._resource_instances[i].process_response()

    @property
    def resource_instances(self):
        return self._resource_instances

    def get_resource_errors(self) -> dict:
        """
        Aggregates all the errors of each instances to the and present to the users
        :return:
        """
        errors = {}
        for res in self._resource_classes.keys():
            errors[res] = getattr(self, res).errors
        return errors

    def aggregate_results(self) -> dict:
        """
        This method aggregates the results of each instance and add them up, return as a dictionary
        :return: results
        """

        results = {
            'Total number of repos': self.aggregate_number_of_repos,
            'Total Watcher count': self.aggregate_watcher_or_follower_count,
            'List/Count of Languages': self.aggregate_repos_languages,
            'List/Count of Repos topics': self.aggregate_repos_topics
        }

        return results

    @property
    def aggregate_number_of_repos(self) -> int:
        """
        :var: total: aggregates the total number of repos of all instances
        :return: total
        """
        total = 0
        for instance in self._resource_instances:
            total += instance.total_number_of_repos
        return total

    @property
    def aggregate_watcher_or_follower_count(self) -> int:
        """
        :var: total: aggregates the total number of followers and watchers of all instances
        :return:
        """
        total = 0
        for instance in self._resource_instances:
            total += instance.total_watcher_or_follower_count
        return total

    @property
    def aggregate_repos_languages(self) -> list:
        """
        :var: langs: find the sets of all languages used across all instances
        :return: list(langs)
        """
        langs = set()
        for instance in self._resource_instances:
            langs = langs.union(instance.list_repos_languages)
        return list(langs)

    @property
    def aggregate_repos_topics(self) -> list:
        """find the list of all repos topics available across all instances

        :return: list
        """

        return []
