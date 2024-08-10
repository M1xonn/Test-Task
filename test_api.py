import unittest
import requests


"""pip install unittest-xml-reporting
    python -m xmlrunner discover -o reports
    Для создания xml файла с отчетом по тестам"""

class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5413/api"

    def setUp(self):
        self.headers = {'Content-Type': 'application/json'}

    def test_state(self):
        response = requests.get(f"{self.BASE_URL}/state")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['statusCode'], 0)
        self.assertEqual(data['state'], 'OК')

    def test_addition(self):
        response = self.send_post_request("addition", 54, 23)
        self.check_response(response, 54 + 23)

    def test_multiplication(self):
        response = self.send_post_request("multiplication", 54, 23)
        self.check_response(response, 54 * 23)

    def test_division(self):
        response = self.send_post_request("division", 54, 23)
        self.check_response(response, 54 // 23)

    def test_remainder(self):
        response = self.send_post_request("remainder", 54, 23)
        self.check_response(response, 54 % 23)

    def test_addition_boundary_value(self):
        response = self.send_post_request("addition", 2147483647, 2147483647)
        self.check_response(response, 2147483647 + 2147483647)

    def test_multiplication_boundary_value(self):
        response = self.send_post_request("multiplication",2147483647, 2147483647)
        self.check_response(response, 2147483647 * 2147483647)

    def test_division_boundary_value(self):
        response = self.send_post_request("division", -2147483648, 4)
        self.check_response(response, -2147483648 // 4)

    def test_remainder_boundary_value(self):
        response = self.send_post_request("remainder", 2147483647, 3)
        self.check_response(response, 2147483647 % 3)

    def send_post_request(self, endpoint, x, y):
        data = {"x": x, "y": y}
        response = requests.post(f"{self.BASE_URL}/{endpoint}", json=data, headers=self.headers)
        return response

    def check_response(self, response, expected_result):
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['statusCode'], 0)
        self.assertEqual(data['result'], expected_result)

    def test_missing_keys(self):
        response = requests.post(f"{self.BASE_URL}/addition", json={"x": 54}, headers=self.headers)
        self.check_error_response(response, 2)

    def test_non_integer_values(self):
        response = requests.post(f"{self.BASE_URL}/addition", json={"x": "54", "y": 23}, headers=self.headers)
        self.check_error_response(response, 3)

    def test_invalid_json_format(self):
        response = requests.post(f"{self.BASE_URL}/addition", data="Invalid JSON", headers=self.headers)
        self.check_error_response(response, 5)

    def test_addition_exceed_value_range(self):
        response = requests.post(f"{self.BASE_URL}/addition", json={"x": 2147483649, "y": 1}, headers=self.headers)
        self.check_error_response(response, 4)

    def test_multiplication_exceed_value_range(self):
        response = requests.post(f"{self.BASE_URL}/multiplication", json={"x": 2147483649, "y": 1}, headers=self.headers)
        self.check_error_response(response, 4)

    def test_division_exceed_value_range(self):
        response = requests.post(f"{self.BASE_URL}/division", json={"x": 2147483649, "y": 1}, headers=self.headers)
        self.check_error_response(response, 4)

    def test_remainder_exceed_value_range(self):
        response = requests.post(f"{self.BASE_URL}/remainder", json={"x": 2147483649, "y": 1}, headers=self.headers)
        self.check_error_response(response, 4)

    def check_error_response(self, response, expected_code):
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['statusCode'], expected_code)


if __name__ == "__main__":
    unittest.main()
