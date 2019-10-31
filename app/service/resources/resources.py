from app.service import APIServiceException, AsyncRequest
from app.service.resources import Resource


class GitHubResource(Resource):
    """
    It subclasses the Resource Class, it is compulsory to initialize the service_connection_endpoints instance variable
    and should have public_repo key and value as the repo url as the public_repo key is used to call the repo_url at the
    Aggregate Resource Class.
    It must also call the base class with the protocol, base url and secure_connection set to True.
    Default secure_connection is False.
    If secure_connection is True and protocol is http, ValueError will be raised.
    It must implement the process_response method else NotImplementedError will be raised

    """

    @staticmethod
    def process_repo(repos):
        # Helper function to help process and loop through repos to get values¿
        watchers_count = 0
        languages = set()
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages.add(lang.capitalize())
            watchers_count += repo.get('watchers_count', 0)

        return watchers_count, languages

    def __init__(self, user):
        base_url = 'https://api.github.com/'
        self.service_connection_endpoints = {'public_repo': 'users/{}/repos'.format(user)}
        super().__init__('https', base_url, True)

    def process_response(self):
        # self.response needs to be set as the response from the request else raises Exception
        # check if response is an exception and pass it as error
        # Check if message is in response and pass it as errors
        # Do not process repos if errors do exist
        if self.response is None:
            raise APIServiceException('Response is invalid')

        if isinstance(self.response, Exception):
            self.errors = str(self.response)
        elif 'message' in self.response:
            self.errors = self.response.get('message')
        if self.errors:
            print(self.errors)
        else:
            # set total repos, total watcher and list repo language
            repos = self.response
            self.total_number_of_repos = len(repos)
            self.total_watcher_or_follower_count, self.list_repos_languages = self.process_repo(repos)

        print('git language: ', self.list_repos_languages)
        print('git repo count:', self.total_number_of_repos)
        print('git followers count', self.total_watcher_or_follower_count)


class BitBucketResource(Resource):
    """"
    This uses the version 2 of the bitbuckets APIS
    It subclasses the Resource Class, it is compulsory to initialize the service_connection_endpoints instance variable
    and should have public_repo key and value as the repo url as the public_repo key is used to call the repo_url at the
    Aggregate Resource Class.
    It must also call the base class with the protocol, base url and secure_connection set to True.
    Default secure_connection is False.
    If secure_connection is True and protocol is http, ValueError will be raised.
    It must implement the process_response method else NotImplementedError will be raised
    """

    # version 2 of bitbucket api
    def __init__(self, user):
        base_url = 'https://bitbucket.org/'
        self.service_connection_endpoints = {'public_repo': '/api/2.0/repositories/{}/'.format(user)}
        super().__init__('https', base_url, True)

    def process_response(self):
        if self.response is None:
            raise APIServiceException('Response is invalid')
        if isinstance(self.response, Exception):
            self.errors = str(self.response)

        elif 'error' in self.response:
            self.errors = self.response.get('error')
        if self.errors:
            print(self.errors)

        # Find the values

        # if not values:
        #     type = self.response.get('type')
        #     msg = self.response.get(type, 'An Error has occured')
        #     self.errors = msg
        else:
            values = self.response.get('values')
            size = self.response.get('size', 0)
            self.total_number_of_repos = size
            watchers_links = []
            languages = set()
            for repo in values:
                lang = repo.get('language')
                if lang:
                    languages.add(lang.capitalize())
                # print(languages)
                links = repo.get('links')
                if links:
                    watchers = links.get('watchers')
                    if watchers:
                        watchers_link = watchers.get('href')
                        watchers_links.append(watchers_link)
            self.list_repos_languages = languages
            async_request = AsyncRequest(watchers_links)
            responses = async_request.run()
            watchers_count = 0
            for res in responses:
                watchers_count += int(res.get('size'))

            self.total_watcher_or_follower_count = watchers_count

        print('bit language: ', self.list_repos_languages)
        print('bit repo count:', self.total_number_of_repos)
        print('bit followers count', self.total_watcher_or_follower_count)


register_resources_classes = {'github': GitHubResource, 'bitbucket': BitBucketResource}
