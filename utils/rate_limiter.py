import time
import random
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.requests = defaultdict(list)
        self.last_request_time = {}
        
    def _get_current_window(self, window_size: int) -> int:
        """Get the current time window."""
        return int(time.time() // window_size)
        
    def _cleanup_old_requests(self, key: str, window_size: int):
        """Remove requests older than the current window."""
        current_window = self._get_current_window(window_size)
        self.requests[key] = [t for t in self.requests[key] 
                            if self._get_current_window(window_size) == current_window]
        
    def _get_delay(self, min_delay: int, max_delay: int) -> float:
        """Get a random delay between min and max values."""
        return random.uniform(min_delay, max_delay)
        
    def check_rate_limit(self, 
                        key: str, 
                        max_requests: int, 
                        window_size: int) -> bool:
        """Check if a request would exceed the rate limit."""
        self._cleanup_old_requests(key, window_size)
        return len(self.requests[key]) < max_requests
        
    def record_request(self, key: str):
        """Record a new request."""
        current_time = time.time()
        self.requests[key].append(current_time)
        self.last_request_time[key] = current_time
        
    def get_wait_time(self, 
                     key: str, 
                     max_requests: int, 
                     window_size: int) -> float:
        """Calculate how long to wait before making the next request."""
        if not self.requests[key]:
            return 0
            
        current_time = time.time()
        window_start = current_time - window_size
        
        # Count requests in current window
        recent_requests = sum(1 for t in self.requests[key] if t > window_start)
        
        if recent_requests >= max_requests:
            # Wait until the oldest request in the window expires
            oldest_request = min(t for t in self.requests[key] if t > window_start)
            return window_start + window_size - current_time
            
        return 0
        
    def wait_if_needed(self, 
                      key: str, 
                      max_requests: int, 
                      window_size: int):
        """Wait if necessary to respect rate limits."""
        wait_time = self.get_wait_time(key, max_requests, window_size)
        if wait_time > 0:
            self.logger.info(f"Rate limit reached for {key}, waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
            
    def get_randomized_delay(self) -> float:
        """Get a randomized delay based on configuration."""
        return self._get_delay(
            self.config['rate_limits']['min_delay_seconds'],
            self.config['rate_limits']['max_delay_seconds']
        )
        
    def enforce_rate_limit(self, 
                          key: str, 
                          max_requests: int, 
                          window_size: int):
        """Enforce rate limiting with randomized delays."""
        # Check if we need to wait due to rate limits
        self.wait_if_needed(key, max_requests, window_size)
        
        # Add randomized delay
        delay = self.get_randomized_delay()
        if delay > 0:
            self.logger.debug(f"Adding randomized delay of {delay:.2f} seconds")
            time.sleep(delay)
            
        # Record the request
        self.record_request(key)
        
    def get_daily_usage(self, key: str) -> Dict:
        """Get daily usage statistics for a key."""
        today = datetime.now().date()
        daily_requests = [t for t in self.requests[key] 
                         if datetime.fromtimestamp(t).date() == today]
        
        return {
            'total_requests': len(daily_requests),
            'first_request': datetime.fromtimestamp(min(daily_requests)).isoformat() 
                           if daily_requests else None,
            'last_request': datetime.fromtimestamp(max(daily_requests)).isoformat() 
                          if daily_requests else None,
            'average_interval': (max(daily_requests) - min(daily_requests)) / len(daily_requests) 
                              if len(daily_requests) > 1 else None
        }
        
    def reset_counters(self):
        """Reset all rate limiting counters."""
        self.requests.clear()
        self.last_request_time.clear()
        self.logger.info("Rate limiting counters reset")
        
    def get_status(self) -> Dict:
        """Get current status of all rate limiters."""
        status = {}
        for key in self.requests:
            status[key] = {
                'total_requests': len(self.requests[key]),
                'last_request': datetime.fromtimestamp(self.last_request_time[key]).isoformat() 
                              if key in self.last_request_time else None,
                'daily_usage': self.get_daily_usage(key)
            }
        return status 