from unittest import TestCase, main
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


if __name__ == '__main__':
    main()
