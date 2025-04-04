import requests
import json
import time
import random
import logging
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class DirectorySubmitter:
    def __init__(self, config_path: str = "backlink_config.json"):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.driver = None
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise

    def _setup_driver(self):
        """Setup Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def _teardown_driver(self):
        """Close Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def submit_to_directory(self, directory: Dict) -> Dict:
        """Submit website to a directory."""
        result = {
            'directory': directory['name'],
            'status': 'failed',
            'message': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if directory.get('requires_selenium', False):
                if not self.driver:
                    self._setup_driver()
                
                self._submit_with_selenium(directory)
            else:
                self._submit_with_requests(directory)
                
            result['status'] = 'success'
            result['message'] = 'Submission successful'
            
        except Exception as e:
            result['message'] = str(e)
            self.logger.error(f"Failed to submit to {directory['name']}: {str(e)}")
            
        finally:
            if directory.get('requires_selenium', False):
                self._teardown_driver()
                
        return result

    def _submit_with_selenium(self, directory: Dict):
        """Submit using Selenium for JavaScript-heavy directories."""
        try:
            self.driver.get(directory['submission_url'])
            
            # Wait for form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, directory['form_id']))
            )
            
            # Fill form fields
            for field, value in directory['form_fields'].items():
                element = self.driver.find_element(By.NAME, field)
                element.send_keys(value)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, directory['submit_button'])
            submit_button.click()
            
            # Wait for success message
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, directory['success_selector']))
            )
            
        except TimeoutException:
            raise Exception("Timeout waiting for page elements")
        except NoSuchElementException:
            raise Exception("Required form elements not found")
        except Exception as e:
            raise Exception(f"Selenium submission failed: {str(e)}")

    def _submit_with_requests(self, directory: Dict):
        """Submit using requests for simple directories."""
        try:
            response = requests.post(
                directory['submission_url'],
                data=directory['form_fields'],
                headers=directory.get('headers', {})
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
            # Verify submission success
            soup = BeautifulSoup(response.text, 'html.parser')
            success_element = soup.select_one(directory['success_selector'])
            
            if not success_element:
                raise Exception("Success message not found in response")
                
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def submit_to_multiple_directories(self, directories: List[Dict]) -> List[Dict]:
        """Submit to multiple directories with rate limiting."""
        results = []
        
        for directory in directories:
            # Add random delay between submissions
            delay = random.uniform(
                self.config['rate_limits']['min_delay_seconds'],
                self.config['rate_limits']['max_delay_seconds']
            )
            time.sleep(delay)
            
            result = self.submit_to_directory(directory)
            results.append(result)
            
            if result['status'] == 'success':
                self.logger.info(f"Successfully submitted to {directory['name']}")
            else:
                self.logger.warning(f"Failed to submit to {directory['name']}: {result['message']}")
        
        return results

    def check_submission_status(self, directory: Dict) -> Dict:
        """Check if website is listed in directory."""
        try:
            response = requests.get(directory['listing_url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for website listing
            listing = soup.select_one(directory['listing_selector'])
            
            return {
                'directory': directory['name'],
                'is_listed': bool(listing),
                'listing_url': directory['listing_url'] if listing else None,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to check status in {directory['name']}: {str(e)}")
            return {
                'directory': directory['name'],
                'is_listed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            } 