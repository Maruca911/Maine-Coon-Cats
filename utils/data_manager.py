import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import pandas as pd

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        try:
            self.data_dir.mkdir(exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating data directory: {str(e)}")
            raise
            
    def save_json(self, data: Any, filename: str) -> bool:
        """Save data to a JSON file."""
        try:
            file_path = self.data_dir / filename
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.info(f"Saved data to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving JSON data: {str(e)}")
            return False
            
    def load_json(self, filename: str) -> Optional[Any]:
        """Load data from a JSON file."""
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return None
                
            with open(file_path, 'r') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in file {filename}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading JSON data: {str(e)}")
            return None
            
    def save_csv(self, data: List[Dict], filename: str) -> bool:
        """Save data to a CSV file."""
        try:
            file_path = self.data_dir / filename
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            
            self.logger.info(f"Saved data to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving CSV data: {str(e)}")
            return False
            
    def load_csv(self, filename: str) -> Optional[pd.DataFrame]:
        """Load data from a CSV file."""
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return None
                
            return pd.read_csv(file_path)
            
        except Exception as e:
            self.logger.error(f"Error loading CSV data: {str(e)}")
            return None
            
    def append_json(self, data: Any, filename: str) -> bool:
        """Append data to a JSON file."""
        try:
            file_path = self.data_dir / filename
            existing_data = []
            
            if file_path.exists():
                existing_data = self.load_json(filename) or []
                
            if isinstance(existing_data, list):
                existing_data.append(data)
            else:
                self.logger.error(f"Cannot append to non-list data in {filename}")
                return False
                
            return self.save_json(existing_data, filename)
            
        except Exception as e:
            self.logger.error(f"Error appending JSON data: {str(e)}")
            return False
            
    def update_json(self, data: Dict, filename: str) -> bool:
        """Update data in a JSON file."""
        try:
            file_path = self.data_dir / filename
            existing_data = {}
            
            if file_path.exists():
                existing_data = self.load_json(filename) or {}
                
            if not isinstance(existing_data, dict):
                self.logger.error(f"Cannot update non-dict data in {filename}")
                return False
                
            existing_data.update(data)
            return self.save_json(existing_data, filename)
            
        except Exception as e:
            self.logger.error(f"Error updating JSON data: {str(e)}")
            return False
            
    def get_latest_file(self, pattern: str) -> Optional[Path]:
        """Get the latest file matching a pattern."""
        try:
            files = list(self.data_dir.glob(pattern))
            if not files:
                return None
                
            return max(files, key=lambda x: x.stat().st_mtime)
            
        except Exception as e:
            self.logger.error(f"Error getting latest file: {str(e)}")
            return None
            
    def backup_file(self, filename: str) -> bool:
        """Create a backup of a file."""
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                self.logger.warning(f"File not found for backup: {file_path}")
                return False
                
            backup_path = file_path.with_suffix('.bak')
            file_path.rename(backup_path)
            
            self.logger.info(f"Created backup of {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            return False
            
    def restore_backup(self, filename: str) -> bool:
        """Restore a file from backup."""
        try:
            file_path = self.data_dir / filename
            backup_path = file_path.with_suffix('.bak')
            
            if not backup_path.exists():
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
                
            if file_path.exists():
                file_path.unlink()
                
            backup_path.rename(file_path)
            
            self.logger.info(f"Restored backup to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {str(e)}")
            return False
            
    def cleanup_old_files(self, pattern: str, days: int = 30) -> bool:
        """Clean up files older than specified days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            files_removed = 0
            
            for file_path in self.data_dir.glob(pattern):
                if datetime.fromtimestamp(file_path.stat().st_mtime) < cutoff_date:
                    file_path.unlink()
                    files_removed += 1
                    
            if files_removed > 0:
                self.logger.info(f"Removed {files_removed} old files")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old files: {str(e)}")
            return False
            
    def get_file_info(self, filename: str) -> Optional[Dict]:
        """Get information about a file."""
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                return None
                
            stat = file_path.stat()
            return {
                'path': str(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': file_path.suffix[1:] if file_path.suffix else 'unknown'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {str(e)}")
            return None
            
    def get_directory_info(self) -> Dict:
        """Get information about the data directory."""
        try:
            total_size = sum(f.stat().st_size for f in self.data_dir.glob('**/*') if f.is_file())
            file_count = sum(1 for _ in self.data_dir.glob('**/*') if _.is_file())
            
            return {
                'path': str(self.data_dir),
                'total_size': total_size,
                'file_count': file_count,
                'files': [
                    self.get_file_info(f.name)
                    for f in self.data_dir.glob('*')
                    if f.is_file()
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting directory info: {str(e)}")
            return {} 