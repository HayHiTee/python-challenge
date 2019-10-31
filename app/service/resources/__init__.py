
from app.service import AsyncRequest, APIServiceException
from app.service.connection import ServiceConnection


class Resource(ServiceConnection):
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





