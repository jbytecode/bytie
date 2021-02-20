from unittest import TestCase, main
from unittest.mock import patch
import bytie.messagehandle

import ast

class TestMessageHandler(TestCase):

    def test_hey_bytie(self):
        self.assertEqual(
            bytie.messagehandle.bytie_handle_hey_bytie(), "Yes, sir!")

    def test_ast(self):
        cmd = "4"
        self.assertEqual(
            bytie.messagehandle.bytie_handle_ast(cmd),
            "Module(body=[Expr(value=Constant(value=4))], type_ignores=[])")

    def test_iplikisyin(self):
        content = "Ama Java'da Multiple Inheritance yok ki"
        result = bytie.messagehandle.bytie_handle_iplikisyin(content)
        iplikisyin = "imi jivi'di miltipli inhiritinci yik ki :rofl:"
        oplokosyon = "omo jovo'do moltoplo onhorotonco yok ko :rofl:"
        self.assertIn(result, [iplikisyin, oplokosyon])

    @patch('requests.get')
    def test_dadjoke_success(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {'id': '12345678', 'joke': 'an absolute unit of a joke'}
        self.assertEqual(
            bytie.messagehandle.bytie_handle_dadjoke(),
            "https://icanhazdadjoke.com/j/12345678.png")

    @patch('requests.get')
    def test_dadjoke_fail(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 400
        self.assertEqual(
            bytie.messagehandle.bytie_handle_dadjoke(),
            "Couldn't get a dadjoke :(")


if __name__ == '__main__':
    main()
