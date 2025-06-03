
import requests
import unittest
import json
from datetime import datetime

class ProductPricingCalculatorAPITest(unittest.TestCase):
    def setUp(self):
        # Get the backend URL from the frontend .env file
        self.base_url = "https://a29e4496-b87a-4267-93f2-c83df6349746.preview.emergentagent.com/api"
        self.session = requests.Session()
        print(f"Testing API at: {self.base_url}")

    def test_01_api_root(self):
        """Test the API root endpoint"""
        print("\n🔍 Testing API root endpoint...")
        response = self.session.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Product Pricing Calculator API")
        print("✅ API root endpoint test passed")

    def test_02_gst_rates(self):
        """Test the GST rates endpoint"""
        print("\n🔍 Testing GST rates endpoint...")
        response = self.session.get(f"{self.base_url}/gst-rates")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("common_rates", data)
        self.assertTrue(len(data["common_rates"]) > 0)
        
        # Verify the common GST rates
        rates = [rate["rate"] for rate in data["common_rates"]]
        expected_rates = [0, 5, 12, 18, 28]
        for rate in expected_rates:
            self.assertIn(rate, rates)
        
        print("✅ GST rates endpoint test passed")

    def test_03_calculation_test_case_1(self):
        """Test calculation with Test Case 1"""
        print("\n🔍 Testing calculation with Test Case 1...")
        test_data = {
            "product_name": "Test Product A",
            "quantity": 10,
            "unit_price_before_tax": 100,
            "gst_percentage": 18,
            "sales_price_mrp_per_unit": 150
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify the calculation results
        self.assertEqual(result["product_name"], "Test Product A")
        self.assertEqual(result["quantity"], 10)
        self.assertEqual(result["unit_price_before_tax"], 100)
        self.assertEqual(result["gst_percentage"], 18)
        self.assertEqual(result["sales_price_mrp_per_unit"], 150)
        
        # Check calculated values
        self.assertEqual(result["subtotal_before_tax"], 1000)
        self.assertEqual(result["unit_price_after_tax"], 118)
        self.assertEqual(result["subtotal_after_tax"], 1180)
        self.assertAlmostEqual(result["margin_percentage"], 21.33, delta=0.01)
        self.assertAlmostEqual(result["markup_percentage"], 27.12, delta=0.01)
        
        print("✅ Test Case 1 calculation test passed")
        return result["calculation_id"]

    def test_04_calculation_test_case_2(self):
        """Test calculation with Test Case 2"""
        print("\n🔍 Testing calculation with Test Case 2...")
        test_data = {
            "product_name": "Test Product B",
            "quantity": 5,
            "unit_price_before_tax": 250,
            "gst_percentage": 5,
            "sales_price_mrp_per_unit": 300
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify the calculation results
        self.assertEqual(result["product_name"], "Test Product B")
        self.assertEqual(result["quantity"], 5)
        self.assertEqual(result["unit_price_before_tax"], 250)
        self.assertEqual(result["gst_percentage"], 5)
        self.assertEqual(result["sales_price_mrp_per_unit"], 300)
        
        # Check calculated values
        self.assertEqual(result["subtotal_before_tax"], 1250)
        self.assertEqual(result["unit_price_after_tax"], 262.5)
        self.assertEqual(result["subtotal_after_tax"], 1312.5)
        self.assertAlmostEqual(result["margin_percentage"], 12.5, delta=0.01)
        self.assertAlmostEqual(result["markup_percentage"], 14.29, delta=0.01)
        
        print("✅ Test Case 2 calculation test passed")
        return result["calculation_id"]

    def test_05_calculation_test_case_3(self):
        """Test calculation with Test Case 3"""
        print("\n🔍 Testing calculation with Test Case 3...")
        test_data = {
            "product_name": "Tax Free Product",
            "quantity": 20,
            "unit_price_before_tax": 50,
            "gst_percentage": 0,
            "sales_price_mrp_per_unit": 60
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify the calculation results
        self.assertEqual(result["product_name"], "Tax Free Product")
        self.assertEqual(result["quantity"], 20)
        self.assertEqual(result["unit_price_before_tax"], 50)
        self.assertEqual(result["gst_percentage"], 0)
        self.assertEqual(result["sales_price_mrp_per_unit"], 60)
        
        # Check calculated values
        self.assertEqual(result["subtotal_before_tax"], 1000)
        self.assertEqual(result["unit_price_after_tax"], 50)
        self.assertEqual(result["subtotal_after_tax"], 1000)
        self.assertAlmostEqual(result["margin_percentage"], 16.67, delta=0.01)
        self.assertAlmostEqual(result["markup_percentage"], 20, delta=0.01)
        
        print("✅ Test Case 3 calculation test passed")
        return result["calculation_id"]

    def test_06_save_calculation_to_history(self):
        """Test saving calculation to history"""
        print("\n🔍 Testing saving calculation to history...")
        # First, perform a calculation
        calc_id = self.test_03_calculation_test_case_1()
        
        # Then, check if it appears in the history
        response = self.session.get(f"{self.base_url}/calculations")
        self.assertEqual(response.status_code, 200)
        history = response.json()
        
        # Verify that the history is not empty
        self.assertTrue(len(history) > 0)
        
        # Check if our calculation is in the history
        found = False
        for entry in history:
            if entry["calculation_result"]["product_name"] == "Test Product A":
                found = True
                break
        
        self.assertTrue(found, "Calculation was not found in history")
        print("✅ Calculation history test passed")

    def test_07_validation_errors(self):
        """Test validation errors"""
        print("\n🔍 Testing validation errors...")
        
        # Test with invalid data (negative quantity)
        test_data = {
            "product_name": "Invalid Product",
            "quantity": -5,
            "unit_price_before_tax": 100,
            "gst_percentage": 18,
            "sales_price_mrp_per_unit": 150
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid GST percentage (over 100%)
        test_data = {
            "product_name": "Invalid Product",
            "quantity": 5,
            "unit_price_before_tax": 100,
            "gst_percentage": 150,
            "sales_price_mrp_per_unit": 150
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 400)
        
        print("✅ Validation errors test passed")

    def test_08_bulk_calculation(self):
        """Test bulk calculation endpoint"""
        print("\n🔍 Testing bulk calculation endpoint...")
        
        test_data = {
            "products": [
                {
                    "product_name": "Bulk Product 1",
                    "quantity": 10,
                    "unit_price_before_tax": 100,
                    "gst_percentage": 18,
                    "sales_price_mrp_per_unit": 150
                },
                {
                    "product_name": "Bulk Product 2",
                    "quantity": 5,
                    "unit_price_before_tax": 250,
                    "gst_percentage": 5,
                    "sales_price_mrp_per_unit": 300
                }
            ]
        }
        
        response = self.session.post(f"{self.base_url}/calculate-bulk", json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify the bulk calculation results
        self.assertEqual(len(result["calculations"]), 2)
        self.assertEqual(result["total_products"], 2)
        
        # Check first product
        self.assertEqual(result["calculations"][0]["product_name"], "Bulk Product 1")
        self.assertEqual(result["calculations"][0]["subtotal_before_tax"], 1000)
        
        # Check second product
        self.assertEqual(result["calculations"][1]["product_name"], "Bulk Product 2")
        self.assertEqual(result["calculations"][1]["subtotal_before_tax"], 1250)
        
        print("✅ Bulk calculation test passed")

    def test_09_review_request_calculation(self):
        """Test calculation with the specific test case from the review request"""
        print("\n🔍 Testing calculation with Review Request Test Case...")
        test_data = {
            "product_name": "Final Test Product",
            "quantity": 8,
            "unit_price_before_tax": 125,
            "gst_percentage": 18,
            "sales_price_mrp_per_unit": 180
        }
        
        response = self.session.post(f"{self.base_url}/calculate", json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify the calculation results
        self.assertEqual(result["product_name"], "Final Test Product")
        self.assertEqual(result["quantity"], 8)
        self.assertEqual(result["unit_price_before_tax"], 125)
        self.assertEqual(result["gst_percentage"], 18)
        self.assertEqual(result["sales_price_mrp_per_unit"], 180)
        
        # Check calculated values against expected results from review request
        self.assertEqual(result["subtotal_before_tax"], 1000)
        self.assertEqual(result["unit_price_after_tax"], 147.5)
        self.assertEqual(result["subtotal_after_tax"], 1180)
        self.assertAlmostEqual(result["margin_percentage"], 18.06, delta=0.01)
        self.assertAlmostEqual(result["markup_percentage"], 22.03, delta=0.01)
        
        # Test saving to history
        # First, get the calculation ID
        calc_id = result["calculation_id"]
        
        # Then, check if it appears in the history
        response = self.session.get(f"{self.base_url}/calculations")
        self.assertEqual(response.status_code, 200)
        history = response.json()
        
        # Verify that the history is not empty
        self.assertTrue(len(history) > 0)
        
        # Check if our calculation is in the history
        found = False
        for entry in history:
            if entry["calculation_result"]["product_name"] == "Final Test Product":
                found = True
                break
        
        self.assertTrue(found, "Calculation was not found in history")
        print("✅ Review Request calculation test passed")
        print("✅ Calculation was successfully saved to history")

if __name__ == "__main__":
    unittest.main(verbosity=2)
