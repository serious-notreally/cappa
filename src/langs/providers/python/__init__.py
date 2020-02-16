import re
import subprocess
import os
import uuid
from django.conf import settings
from .utils import TmpFile
from ..base import BaseProvider
from src.tasks.models import Task


class Provider(BaseProvider):

    class TmpFile:

        def __init__(self, content):
            self.filename = "%s.py" % (uuid.uuid4())
            self.filedir = os.path.join(settings.TMP_DIR, self.filename)
            file = open(self.filedir, "wb")
            file.write(bytes(content, 'utf-8'))
            file.close()

        def remove(self):
            os.remove(self.filedir)
            return True

    @staticmethod
    def debug(input: str, content: str) -> dict:
        stdin = bytes(input, 'utf-8')
        tmp_file = TmpFile(content)
        proc = subprocess.Popen(
            args=[settings.PYTHON_PATH, tmp_file.filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )

        stdout, stderr = proc.communicate(stdin)
        tmp_file.remove()
        proc.kill()
        return {
            'output': stdout.decode("utf-8"),
            'error': re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
        }

    @staticmethod
    def check_tests(content: str, tests: list, output_type: Task.OUTPUT_TYPES) -> dict:
        tmp_file = TmpFile(content)
        args = [settings.PYTHON_PATH, tmp_file.filename]
        tests_data = []
        tests_num = len(tests)
        tests_num_success = 0
        check_test = getattr(Provider, f'_check_{output_type}')
        for i in range(len(tests)):
            proc = subprocess.Popen(
                args=args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR,
            )
            stdin = bytes(tests[i]['input'], 'utf-8')
            stdout, stderr = proc.communicate(stdin)
            output = stdout.decode("utf-8")
            error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))

            success = False if error else check_test(val=output, test_val=tests[i]['output'])
            if success:
                tests_num_success += 1

            tests_data.append({
                "output": output,
                "error": error,
                "success": success
            })
            proc.kill()

        tmp_file.remove()

        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': bool(tests_num == tests_num_success),
        }