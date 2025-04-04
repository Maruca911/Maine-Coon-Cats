import json
import logging
import logging.config
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime, timedelta

class LoggingManager:
    def __init__(self, config_path: str = "logging_config.json"):
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        self._setup_logging()
        
    def _load_config(self) -> Dict:
        """Load logging configuration from JSON file."""
        try:
            if not self.config_path.exists():
                self.logger.warning(f"Logging configuration file not found: {self.config_path}")
                return self._get_default_config()
                
            with open(self.config_path, 'r') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in logging configuration: {str(e)}")
            return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading logging configuration: {str(e)}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict:
        """Get default logging configuration."""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'filename': 'logs/backlink_automation.log',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                    'encoding': 'utf8'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'INFO',
                    'propagate': True
                }
            }
        }
        
    def _setup_logging(self):
        """Setup logging configuration."""
        try:
            # Create logs directory if it doesn't exist
            logs_dir = Path('logs')
            logs_dir.mkdir(exist_ok=True)
            
            # Apply logging configuration
            logging.config.dictConfig(self.config)
            
        except Exception as e:
            self.logger.error(f"Error setting up logging: {str(e)}")
            
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the specified name."""
        return logging.getLogger(name)
        
    def set_level(self, level: str):
        """Set the logging level for all loggers."""
        try:
            level = level.upper()
            if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                raise ValueError(f"Invalid logging level: {level}")
                
            # Update root logger
            logging.getLogger().setLevel(level)
            
            # Update all handlers
            for handler in logging.getLogger().handlers:
                handler.setLevel(level)
                
            self.logger.info(f"Logging level set to {level}")
            
        except Exception as e:
            self.logger.error(f"Error setting logging level: {str(e)}")
            
    def add_file_handler(self, 
                        filename: str, 
                        level: str = 'DEBUG',
                        max_bytes: int = 10485760,
                        backup_count: int = 5):
        """Add a new file handler."""
        try:
            handler = logging.handlers.RotatingFileHandler(
                filename=filename,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf8'
            )
            
            handler.setLevel(level)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            
            logging.getLogger().addHandler(handler)
            self.logger.info(f"Added file handler for {filename}")
            
        except Exception as e:
            self.logger.error(f"Error adding file handler: {str(e)}")
            
    def rotate_logs(self):
        """Rotate all log files."""
        try:
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.doRollover()
                    
            self.logger.info("Log files rotated")
            
        except Exception as e:
            self.logger.error(f"Error rotating log files: {str(e)}")
            
    def get_log_file_path(self, handler_name: Optional[str] = None) -> Optional[str]:
        """Get the path of a log file."""
        try:
            for handler in logging.getLogger().handlers:
                if (isinstance(handler, logging.handlers.RotatingFileHandler) and
                    (handler_name is None or handler.name == handler_name)):
                    return handler.baseFilename
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting log file path: {str(e)}")
            return None
            
    def cleanup_old_logs(self, days: int = 30):
        """Clean up log files older than specified days."""
        try:
            logs_dir = Path('logs')
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for log_file in logs_dir.glob('*.log*'):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    self.logger.info(f"Removed old log file: {log_file}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up old logs: {str(e)}")
            
    def get_logging_status(self) -> Dict:
        """Get current logging status."""
        status = {
            'root_level': logging.getLogger().level,
            'handlers': [],
            'log_files': []
        }
        
        for handler in logging.getLogger().handlers:
            handler_info = {
                'type': handler.__class__.__name__,
                'level': handler.level,
                'formatter': handler.formatter.__class__.__name__ if handler.formatter else None
            }
            
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler_info['filename'] = handler.baseFilename
                handler_info['max_bytes'] = handler.maxBytes
                handler_info['backup_count'] = handler.backupCount
                
            status['handlers'].append(handler_info)
            
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                log_file = Path(handler.baseFilename)
                if log_file.exists():
                    status['log_files'].append({
                        'path': str(log_file),
                        'size': log_file.stat().st_size,
                        'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
                    })
                    
        return status 