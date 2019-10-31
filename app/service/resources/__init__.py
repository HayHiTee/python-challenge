from app.service import AsyncRequest, APIServiceException
from app.service.connection import ServiceConnection


class Resource(ServiceConnection):
    """
        It subclasses the Service Connection, it is compulsory to initialize the service_connection_endpoints instance variable
        and should have public_repo key and value as the repo url as the public_repo key is used to call the repo_url at the
        Aggregate Resource Class.
        It must also call the base class with the protocol, base url and secure_connection set to True.
        Default secure_connection is False.
        If secure_connection is True and protocol is http, ValueError will be raised.
        It must implement the process_response method else NotImplementedError will be raised
        If the response instance variable is not set, an error is called
        :ivar:_response: The response of the requests
        :ivar:_languages: unique langauge used across repos
        :ivar:_repo_count: total no of repo
        :ivar:_list_repo_topic: list all the topic in the repo
        :ivar:_watchers_count: total no of watchers
        :ivar: errors: Errors message
        """

    def __init__(self, protocol, base_url, secure_connection=False):
        super().__init__(protocol, base_url, secure_connection)
        self._response = None
        self._languages = set()
        self._repo_count = 0
        self._list_repo_topic = []
        self._watchers_count = 0
        self.errors = None

    def get_repo_url(self, repo_key):
        return self.get_service_connection_url(repo_key)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def process_response(self):
        if self._response is None:
            raise APIServiceException('Response is invalid')

        # implement and process response
        raise NotImplementedError

    @property
    def total_number_of_repos(self) -> int:
        return self._repo_count

    @total_number_of_repos.setter
    def total_number_of_repos(self, value: int):
        self._repo_count = value

    @property
    def total_watcher_or_follower_count(self) -> int:
        return self._watchers_count

    @total_watcher_or_follower_count.setter
    def total_watcher_or_follower_count(self, value: int):
        self._watchers_count = value

    @property
    def list_repos_languages(self) -> set:
        return self._languages

    @list_repos_languages.setter
    def list_repos_languages(self, value: set):
        self._languages = value

    @property
    def list_repos_topics(self) -> list:
        pass

    @list_repos_topics.setter
    def list_repos_topics(self, value: list):
        pass
