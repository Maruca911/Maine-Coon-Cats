import json
import time
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from .email_handler import EmailHandler

class OutreachHandler:
    def __init__(self, config_path: str = "backlink_config.json"):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.email_handler = EmailHandler(config_path)
        
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

    def _load_template(self, template_name: str) -> str:
        """Load email template from file."""
        try:
            template_path = Path("templates") / f"{template_name}.html"
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Template file not found: {template_path}")
            raise

    def _prepare_template_vars(self, 
                             recipient: Dict, 
                             template_type: str) -> Dict:
        """Prepare variables for email template."""
        current_year = datetime.now().year
        resources = self.config['resources']
        
        # Format resources list
        resources_list = ""
        for resource in resources:
            resources_list += f"- {resource['title']}: {resource['url']}\n"
        
        base_vars = {
            'current_year': current_year,
            'resources_list': resources_list,
            'website_name': self.config['website_name'],
            'website_url': self.config['website_url'],
            'contact_email': self.config['contact_email']
        }
        
        if template_type == 'vet_clinic':
            return {
                **base_vars,
                'clinic_name': recipient['name'],
                'location': recipient['location'],
                'subject': 'Free Cat Care Resources for Your Clients'
            }
        elif template_type == 'pet_blogger':
            return {
                **base_vars,
                'blogger_name': recipient['name'],
                'blog_name': recipient['website'],
                'blogger_niche': recipient['niche'],
                'subject': 'Collaboration Opportunity - Cat Care Resources'
            }
        else:
            raise ValueError(f"Unknown template type: {template_type}")

    def send_vet_clinic_outreach(self, clinic: Dict) -> Dict:
        """Send outreach email to a veterinary clinic."""
        result = {
            'clinic': clinic['name'],
            'status': 'failed',
            'message': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            template_vars = self._prepare_template_vars(clinic, 'vet_clinic')
            success = self.email_handler.send_template_email(
                'vet_clinic',
                clinic['email'],
                template_vars
            )
            
            if success:
                result['status'] = 'success'
                result['message'] = 'Email sent successfully'
            else:
                result['message'] = 'Failed to send email'
                
        except Exception as e:
            result['message'] = str(e)
            self.logger.error(f"Failed to send outreach to {clinic['name']}: {str(e)}")
            
        return result

    def send_blogger_outreach(self, blogger: Dict) -> Dict:
        """Send outreach email to a pet blogger."""
        result = {
            'blogger': blogger['name'],
            'status': 'failed',
            'message': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            template_vars = self._prepare_template_vars(blogger, 'pet_blogger')
            success = self.email_handler.send_template_email(
                'pet_blogger',
                blogger['email'],
                template_vars
            )
            
            if success:
                result['status'] = 'success'
                result['message'] = 'Email sent successfully'
            else:
                result['message'] = 'Failed to send email'
                
        except Exception as e:
            result['message'] = str(e)
            self.logger.error(f"Failed to send outreach to {blogger['name']}: {str(e)}")
            
        return result

    def send_bulk_outreach(self, 
                          recipients: List[Dict], 
                          recipient_type: str) -> List[Dict]:
        """Send outreach emails to multiple recipients with rate limiting."""
        results = []
        
        for recipient in recipients:
            # Add random delay between emails
            delay = random.uniform(
                self.config['rate_limits']['min_delay_seconds'],
                self.config['rate_limits']['max_delay_seconds']
            )
            time.sleep(delay)
            
            if recipient_type == 'vet_clinic':
                result = self.send_vet_clinic_outreach(recipient)
            elif recipient_type == 'pet_blogger':
                result = self.send_blogger_outreach(recipient)
            else:
                raise ValueError(f"Unknown recipient type: {recipient_type}")
                
            results.append(result)
            
            if result['status'] == 'success':
                self.logger.info(f"Successfully sent outreach to {recipient['name']}")
            else:
                self.logger.warning(f"Failed to send outreach to {recipient['name']}: {result['message']}")
        
        return results

    def track_response(self, 
                      recipient: Dict, 
                      response: Dict) -> Dict:
        """Track and log response from outreach recipient."""
        result = {
            'recipient': recipient['name'],
            'response_type': response.get('type', 'unknown'),
            'response_date': datetime.now().isoformat(),
            'details': response.get('details', '')
        }
        
        try:
            # Save response to database or file
            response_path = Path("data") / "responses.json"
            responses = []
            
            if response_path.exists():
                with open(response_path, 'r') as f:
                    responses = json.load(f)
            
            responses.append(result)
            
            with open(response_path, 'w') as f:
                json.dump(responses, f, indent=2)
                
            self.logger.info(f"Recorded response from {recipient['name']}")
            
        except Exception as e:
            self.logger.error(f"Failed to track response from {recipient['name']}: {str(e)}")
            
        return result 