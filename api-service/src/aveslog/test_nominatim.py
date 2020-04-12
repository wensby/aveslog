from unittest import TestCase, mock

from aveslog.nominatim import Nominatim


class MockResponse:
  def __init__(self, json_data, status_code):
    self.json_data = json_data
    self.status_code = status_code

  def json(self):
    return self.json_data


class TestNominatim(TestCase):

  def setUp(self):
    self.nominatim = Nominatim()

  @mock.patch('requests.get', side_effect=[MockResponse({'key': 'value'}, 200)])
  def test_reverse(self, mock_get):
    result = self.nominatim.reverse(10, 9, 17, 'en-EN')

    self.assertListEqual(mock_get.call_args_list, [
      mock.call(
        'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=10&lon=9&zoom=17&accept-language=en-EN',
        headers={'User-Agent': 'Aveslog.com'}
      )
    ])
    self.assertDictEqual(result, {'key': 'value'})

  @mock.patch('requests.get', side_effect=[MockResponse({}, 400)])
  def test_reverse_when_response_not_ok(self, mock_get):
    result = self.nominatim.reverse(10, 9, 17, 'en-EN')

    self.assertListEqual(mock_get.call_args_list, [
      mock.call(
        'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=10&lon=9&zoom=17&accept-language=en-EN',
        headers={'User-Agent': 'Aveslog.com'}
      )
    ])
    self.assertIsNone(result)