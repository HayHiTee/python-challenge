import asyncio

import aiohttp
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from app.routes import create_app
from app.service import APIServiceException, AsyncRequest, RestEndpoint, MixinEndpoint
from app.service.connection import ServiceConnection
import unittest

from app.service.resources import Resource
from app.service.resources.aggregate import AggregateResources
from app.service.resources.resources import GitHubResource, BitBucketResource


class RestEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_rest_endpoints = RestEndpoint()
        self.test_first_domain = 'https://www.google.com'

    def test_dispatch(self):
        print(self.test_rest_endpoints.methods)
        self.assertRaises(HTTPMethodNotAllowed, asyncio.run,
                          self.test_rest_endpoints.dispatch('get', self.test_first_domain))

    def tearDown(self):
        pass


class MixinEndpointTestCase(unittest.TestCase):

    def test_dispatch(self):
        async def fetch():
            async with aiohttp.ClientSession() as session:
                urls = ['https://www.google.com', 'https://www.twitter.com']
                self.endpoint = MixinEndpoint(session)
                results = await asyncio.gather(*[self.endpoint.dispatch('get', url) for url in urls],
                                               return_exceptions=True)
                return results

        print(asyncio.run(fetch()))


class AsyncRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.test_urls = [
            'https://api.github.com/users/hayhitee/repos', 'https://bitbucket.org/api/2.0/repositories/hayhitee/']

        self.test_async_request = AsyncRequest(self.test_urls)

    def test_run(self):
        self.assertEqual(len(self.test_async_request.run()), 2)


class ServiceConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.test_first_domain = 'https://www.test.org'
        self.test_second_domain = 'http://www.test.org'
        self.test_third_domain = 'https://www.test.org/api/'
        self.test_service_connection_one = ServiceConnection('https', self.test_first_domain, True)
        self.test_service_connection_two = ServiceConnection('http', self.test_second_domain, False)

        self.test_service_connection_four = ServiceConnection('https', self.test_third_domain, True)
        self.test_service_endpoints = {
            'get_test': '/test/get'
        }
        self.test_service_connection_two.service_connection_endpoints = self.test_service_endpoints

        pass

    def tearDown(self):
        pass

    def test_protocol(self):
        self.assertRaises(ValueError, ServiceConnection, 'http', self.test_first_domain, True)

    def test_base_url(self):
        self.assertEqual(self.test_service_connection_one.base_url, self.test_first_domain)
        self.assertEqual(self.test_service_connection_two.base_url, self.test_second_domain)
        self.assertEqual(self.test_service_connection_four.base_url, self.test_third_domain)

    def test_service_connection_endpoints(self):
        self.assertDictEqual(self.test_service_connection_one.service_connection_endpoints, {})
        self.assertDictEqual(self.test_service_connection_two.service_connection_endpoints, self.test_service_endpoints)

    def test_get_service_connection_url(self):
        self.assertEqual(self.test_service_connection_one.get_service_connection_url(''), self.test_first_domain)
        self.assertEqual(self.test_service_connection_two.get_service_connection_url('get_test'),
                         'http://www.test.org/test/get')


class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.test_first_domain = 'https://www.test.org'
        self.test_resource = Resource('https', self.test_first_domain, True)
        self.test_service_endpoints = {
            'repo_test': '/repo/user'
        }

        self.test_resource.service_connection_endpoints = self.test_service_endpoints

    def tearDown(self):
        pass

    def test_get_repo_url(self):
        self.assertEqual(self.test_resource.get_repo_url('repo_test'), 'https://www.test.org/repo/user')

    def test_process_response(self):
        if self.test_resource.response is None:
            self.assertRaises(APIServiceException, self.test_resource.process_response)
        self.test_resource.response = ''
        self.assertRaises(NotImplementedError, self.test_resource.process_response)

    def test_total_number_of_repos(self):
        self.assertEqual(self.test_resource.total_number_of_repos, 0)

    def test_total_watcher_or_follower_count(self):
        self.assertEqual(self.test_resource.total_watcher_or_follower_count, 0)

    def test_list_repos_languages(self):
        self.assertEqual(self.test_resource.list_repos_languages, set())


class GitHubResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.user = 'mailchimp'
        self.test_github_resource = GitHubResource(self.user)
        self.test_github_base_url = 'https://api.github.com/'
        self.test_repo_url = 'https://api.github.com/users/{}/repos'.format(self.user)
        self.test_async_request = AsyncRequest(self.test_github_resource.get_repo_url('public_repo'))

    def tearDown(self):
        pass

    def test_get_repo_url(self):
        self.assertEqual(self.test_github_resource.get_repo_url('public_repo'), self.test_repo_url)

    def test_process_response(self):
        if self.test_github_resource.response is None:
            self.assertRaises(APIServiceException, self.test_github_resource.process_response)

        self.test_github_resource.response = self.test_async_request.run()

    def test_total_number_of_repos(self):
        self.assertIsInstance(self.test_github_resource.total_number_of_repos, int)

    def test_total_watcher_or_follower_count(self):
        self.assertIsInstance(self.test_github_resource.total_watcher_or_follower_count, int)

    def test_list_repos_languages(self):
        self.assertIsInstance(self.test_github_resource.list_repos_languages, set)


class BitBucketResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.user = 'mailchimp'
        self.test_bitbucket_resource = BitBucketResource(self.user)
        self.test_github_base_url = 'https://bitbucket.org/'
        self.test_repo_url = 'https://bitbucket.org/api/2.0/repositories/{}/'.format(self.user)
        self.test_async_request = AsyncRequest(self.test_bitbucket_resource.get_repo_url('public_repo'))

    def tearDown(self):
        pass

    def test_get_repo_url(self):
        self.assertEqual(self.test_bitbucket_resource.get_repo_url('public_repo'), self.test_repo_url)

    def test_process_response(self):
        if self.test_bitbucket_resource.response is None:
            self.assertRaises(APIServiceException, self.test_bitbucket_resource.process_response)

        self.test_bitbucket_resource.response = self.test_async_request.run()

    def test_total_number_of_repos(self):
        self.assertIsInstance(self.test_bitbucket_resource.total_number_of_repos, int)

    def test_total_watcher_or_follower_count(self):
        self.assertIsInstance(self.test_bitbucket_resource.total_watcher_or_follower_count, int)

    def test_list_repos_languages(self):
        self.assertIsInstance(self.test_bitbucket_resource.list_repos_languages, set)


class FakeResource:
    pass


class AggregateTestCases(unittest.TestCase):
    def setUp(self):
        self.user = 'mailchimp'
        self.test_resource_classes_config = {'github': GitHubResource, 'bitbucket': BitBucketResource}
        self.test_aggregate_resource = AggregateResources(self.user, self.test_resource_classes_config)
        self.test_github_resource = GitHubResource(self.user)
        self.test_bitbucket_resource = BitBucketResource(self.user)
        self.test_urls = [self.test_github_resource.get_repo_url('public_repo'),
                          self.test_bitbucket_resource.get_repo_url('public_repo')]
        self.test_async_request = AsyncRequest(self.test_urls)

        self.test_aggregate_resource.process_resources()
        self.test_github_resource.response, self.test_bitbucket_resource.response = self.test_async_request.run()
        self.test_github_resource.process_response()
        self.test_github_resource.process_response()

    def tearDown(self):
        pass

    def test_fake_resource(self):
        test_fake_resource_classes_config = {'github': GitHubResource, 'bitbucket': BitBucketResource,
                                             'fake': FakeResource}
        self.assertRaises(AssertionError, AggregateResources, self.user, test_fake_resource_classes_config)

    def test_resource_instances(self):
        self.assertIsInstance(self.test_aggregate_resource.resource_instances, list)
        self.assertEqual(len(self.test_aggregate_resource.resource_instances), 2)
        self.assertIsInstance(self.test_aggregate_resource.resource_instances[0], GitHubResource)
        self.assertIsInstance(self.test_aggregate_resource.resource_instances[1], BitBucketResource)

    def test_get_resource_errors(self):
        self.assertIsInstance(self.test_aggregate_resource.get_resource_errors(), dict)
        errors = dict()
        errors['github'] = self.test_github_resource.errors
        errors['bitbucket'] = self.test_github_resource.errors
        self.assertEqual(self.test_aggregate_resource.get_resource_errors(), errors)

    def test_aggregate_results(self):
        self.assertIsInstance(self.test_aggregate_resource.aggregate_results(), dict)
        results = {
            'Total number of repos': self.test_github_resource.total_number_of_repos + self.test_bitbucket_resource.total_number_of_repos,
            'Total Watcher count': self.test_github_resource.total_watcher_or_follower_count + self.test_github_resource.total_watcher_or_follower_count,
            'List/Count of Languages': list(self.test_github_resource.list_repos_languages.union(
                self.test_bitbucket_resource.list_repos_languages)),
            'List/Count of Repos topics': []
        }


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_fetch_good_data(self):
        # data
        res = self.client.get('/users/deolu-asenuga',
                              follow_redirects=True)
        # print(r.content)
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_fetch_bad_data(self):
        # data
        res = self.client.get('/users',
                              follow_redirects=True)
        # print(r.content)
        # print(res.data)
        self.assertEqual(res.status_code, 404)



if __name__ == '__main__':
    unittest.main()