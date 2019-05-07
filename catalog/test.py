from unittest import TestCase

from toscaparser.tosca_template import ToscaTemplate

TEST_URL = "E:\\"
class My_test(TestCase):

    def test_parse_package(self):

        csar_file = "targeted-service-EnhanceService-csar.csar"
        file_names = TEST_URL + csar_file
        tosca = ToscaTemplate(path=file_names,
                              parsed_params=None,
                              no_required_paras_check=True,
                              debug_mode=True)

        self.assertIsNotNone(tosca)