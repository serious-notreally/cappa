from src.tasks.models import Task


class BaseProvider(object):

    """ Реализует обязательные методы провайдера языка программирования """

    @staticmethod
    def _check_str(val: str, test_val: str) -> bool:
        return val == test_val

    @staticmethod
    def _check_int(val: str, test_val: str) -> bool:
        return int(val) == int(test_val)

    @staticmethod
    def _check_float(val: str, test_val: str) -> bool:
        return float(val) == float(test_val)

    @staticmethod
    def debug(input: str, content: str) -> dict:

        # code here

        return {
            "output": "str",
            "error": "str"
        }

    @staticmethod
    def check_tests(content: str, tests: list, output_type: Task.OUTPUT_TYPES) -> dict:

        # code here

        return {
            'num': "int",
            'num_success': "int",
            'success': "bool",
            'tests_data': """[
                {
                    "output": "str",
                    "error": "str,
                    "success": "bool"
                },
                {
                    "output": "str",
                    "error": "str,
                    "success": "bool"
                }, 
                ...
            ]"""
        }
