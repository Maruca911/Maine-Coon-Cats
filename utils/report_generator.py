import json
import logging
from typing import Dict, List
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ReportGenerator:
    def __init__(self, config_path: str = "backlink_config.json"):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        
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
        """Load report template from file."""
        try:
            template_path = Path("reports") / f"{template_name}.html"
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Template file not found: {template_path}")
            raise

    def _prepare_report_data(self, 
                           directory_results: List[Dict],
                           outreach_results: List[Dict]) -> Dict:
        """Prepare data for report generation."""
        # Calculate statistics
        total_submissions = len(directory_results) + len(outreach_results)
        successful_submissions = sum(1 for r in directory_results + outreach_results 
                                   if r['status'] == 'success')
        failed_submissions = total_submissions - successful_submissions
        
        # Format directory submissions table
        directory_rows = []
        for result in directory_results:
            directory_rows.append(
                f"<tr><td>{result['directory']}</td>"
                f"<td class='{result['status']}'>{result['status']}</td>"
                f"<td>{result['timestamp']}</td>"
                f"<td>{result['message']}</td></tr>"
            )
        
        # Format outreach results table
        outreach_rows = []
        for result in outreach_results:
            recipient_type = 'vet_clinic' if 'clinic' in result else 'pet_blogger'
            recipient_name = result.get('clinic', result.get('blogger', 'Unknown'))
            outreach_rows.append(
                f"<tr><td>{recipient_name}</td>"
                f"<td>{recipient_type}</td>"
                f"<td class='{result['status']}'>{result['status']}</td>"
                f"<td>{result['timestamp']}</td>"
                f"<td>{result['message']}</td></tr>"
            )
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_submissions': total_submissions,
            'successful_submissions': successful_submissions,
            'failed_submissions': failed_submissions,
            'success_rate': (successful_submissions / total_submissions * 100) 
                           if total_submissions > 0 else 0,
            'directory_submissions': '\n'.join(directory_rows),
            'outreach_results': '\n'.join(outreach_rows)
        }

    def generate_html_report(self, 
                           directory_results: List[Dict],
                           outreach_results: List[Dict]) -> str:
        """Generate HTML report from results."""
        try:
            template = self._load_template('report_template')
            report_data = self._prepare_report_data(directory_results, outreach_results)
            
            # Replace placeholders in template
            for key, value in report_data.items():
                template = template.replace(f"{{{key}}}", str(value))
            
            # Save report
            report_path = Path("reports") / f"backlink_report_{datetime.now().strftime('%Y%m%d')}.html"
            with open(report_path, 'w') as f:
                f.write(template)
                
            self.logger.info(f"Generated HTML report: {report_path}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            raise

    def generate_statistics_report(self, 
                                 directory_results: List[Dict],
                                 outreach_results: List[Dict]) -> str:
        """Generate statistics report with visualizations."""
        try:
            # Create DataFrame from results
            df = pd.DataFrame(directory_results + outreach_results)
            
            # Generate visualizations
            plt.figure(figsize=(12, 6))
            
            # Success rate by type
            plt.subplot(1, 2, 1)
            success_by_type = df.groupby('type')['status'].value_counts(normalize=True).unstack()
            success_by_type.plot(kind='bar', stacked=True)
            plt.title('Success Rate by Submission Type')
            plt.xlabel('Submission Type')
            plt.ylabel('Percentage')
            
            # Daily submission trend
            plt.subplot(1, 2, 2)
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            daily_trend = df.groupby('date').size()
            daily_trend.plot(kind='line')
            plt.title('Daily Submission Trend')
            plt.xlabel('Date')
            plt.ylabel('Number of Submissions')
            
            # Save plot
            plot_path = Path("reports") / f"statistics_{datetime.now().strftime('%Y%m%d')}.png"
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()
            
            # Generate statistics summary
            stats = {
                'total_submissions': len(df),
                'success_rate': (df['status'] == 'success').mean() * 100,
                'average_response_time': None,  # Calculate if response times are available
                'top_performing_directories': df[df['status'] == 'success']['directory'].value_counts().head(5).to_dict(),
                'conversion_rates': {
                    'directory': (df[df['type'] == 'directory']['status'] == 'success').mean() * 100,
                    'vet_clinic': (df[df['type'] == 'vet_clinic']['status'] == 'success').mean() * 100,
                    'pet_blogger': (df[df['type'] == 'pet_blogger']['status'] == 'success').mean() * 100
                }
            }
            
            # Save statistics
            stats_path = Path("reports") / f"statistics_{datetime.now().strftime('%Y%m%d')}.json"
            with open(stats_path, 'w') as f:
                json.dump(stats, f, indent=2)
                
            self.logger.info(f"Generated statistics report: {stats_path}")
            return str(stats_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate statistics report: {str(e)}")
            raise

    def generate_weekly_summary(self) -> str:
        """Generate weekly summary report."""
        try:
            # Load all reports from the past week
            reports_dir = Path("reports")
            weekly_reports = []
            
            for report_path in reports_dir.glob("backlink_report_*.html"):
                report_date = datetime.strptime(report_path.stem.split('_')[-1], '%Y%m%d')
                if (datetime.now() - report_date).days <= 7:
                    with open(report_path, 'r') as f:
                        weekly_reports.append(f.read())
            
            if not weekly_reports:
                raise Exception("No reports found for the past week")
            
            # Generate summary
            summary = {
                'total_submissions': sum(len(report) for report in weekly_reports),
                'success_rate': sum(1 for report in weekly_reports 
                                  if 'status: success' in report) / len(weekly_reports) * 100,
                'top_performing_directories': {},  # Calculate from reports
                'recommendations': self._generate_recommendations(weekly_reports)
            }
            
            # Save summary
            summary_path = Path("reports") / f"weekly_summary_{datetime.now().strftime('%Y%m%d')}.json"
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
                
            self.logger.info(f"Generated weekly summary: {summary_path}")
            return str(summary_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate weekly summary: {str(e)}")
            raise

    def _generate_recommendations(self, reports: List[str]) -> List[str]:
        """Generate recommendations based on report analysis."""
        recommendations = []
        
        # Analyze success rates
        success_rate = sum(1 for report in reports if 'status: success' in report) / len(reports)
        if success_rate < 0.5:
            recommendations.append("Consider revising outreach templates to improve response rates")
        
        # Analyze directory performance
        directory_success = sum(1 for report in reports 
                              if 'directory' in report and 'status: success' in report)
        if directory_success < len(reports) * 0.3:
            recommendations.append("Review directory submission process and requirements")
        
        # Analyze outreach timing
        morning_submissions = sum(1 for report in reports 
                                if 'timestamp' in report and 
                                datetime.strptime(report['timestamp'], '%Y-%m-%dT%H:%M:%S').hour < 12)
        if morning_submissions < len(reports) * 0.4:
            recommendations.append("Consider scheduling more submissions during morning hours")
        
        return recommendations 