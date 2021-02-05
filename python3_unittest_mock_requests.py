#!/bin/env python3

# https://stackoverflow.com/a/31595270

from unittest import mock, TestCase


class SomeRequestsTests(TestCase):

    def setUp(self):
        # patch the requests module in the corresponding file.
        # must be the path to the file, where the `requests` is imported
        # and where the tested function is
        patcher = mock.patch('module.file.class.requests')
        # mock the response object with some default arguments
        self.mock_response = mock.Mock(status_code=200)
        # ???
        self.mock_response.raise_for_status.return_value = None
        # mock the return value of the corresponding response method
        # in this case - `json()`
        self.mock_response.json.return_value = {}
        # assign the mocked response to the request object / start patching
        self.mock_request = patcher.start()
        # set the return value of the response to the mocked response
        self.mock_request.return_value = self.mock_response

    # stop patching, when all the test finished
    def tearDown(self):
        self.mock_request.stop()

    def test_request_token(self):
        '''Testing a function, which requests a token
        from an API and returns a dict.'''
        # set test data
        at_time = datetime.now(pytz.utc)
        testdata = {
            'accessToken': 'new-access-token',
            'accessTokenExpiration': at_time,
            'refreshToken': 'new-refresh-token',
            'refreshTokenExpiration': at_time,
        }
        # set the return value of the `post()` method of the request to the
        # mocked response
        self.mock_request.post.return_value = self.mock_response
        # overwrite the default return value of the `json()` method of the 
        # mocked response
        self.mock_response.json.return_value = testdata
        # assert
        self.assertEqual(testdata.get('accessToken'),
                         obj.request_token().get('accessToken'))
