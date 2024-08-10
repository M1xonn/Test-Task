import unittest
import subprocess
import time

"""pip install unittest-xml-reporting
    python -m xmlrunner discover -o reports
    Для создания xml файла с отчетом по тестам"""


class TestAppManagement(unittest.TestCase):
    executable_path = r"C:\Users\maxon\webcalculator.exe"

    def start_application(self, host=None, port=None):
        command = [self.executable_path, "start"]
        if host:
            command.append(host)
        if port:
            command.append(str(port))

        subprocess.run(command)
        time.sleep(2)

    def stop_application(self):
        command = [self.executable_path, "stop"]
        subprocess.run(command)
        time.sleep(2)

    def restart_application(self):
        command = [self.executable_path, "restart"]
        subprocess.run(command)
        time.sleep(2)

    def test_default_start(self):
        self.start_application()
        response = subprocess.run(["curl", "http://127.0.0.1:17678/api/state"], capture_output=True, text=True)
        self.assertIn('"state": "O\\u041a"', response.stdout)
        self.stop_application()

    def test_custom_start(self):
        self.start_application(host="localhost", port=5413)
        response = subprocess.run(["curl", "http://localhost:5413/api/state"], capture_output=True, text=True)
        self.assertIn('"state": "O\\u041a"', response.stdout)
        self.stop_application()

    def test_restart(self):
        self.start_application(host="localhost", port=5413)
        self.restart_application()
        response = subprocess.run(["curl", "http://localhost:5413/api/state"], capture_output=True, text=True)
        self.assertIn('"state": "O\\u041a"', response.stdout)
        self.stop_application()

    def test_help(self):
        response = subprocess.run([self.executable_path, "--help"], capture_output=True, text=True)
        self.assertIn("usage:", response.stdout.lower())


if __name__ == "__main__":
    unittest.main()
