"""
Rate limiting utilities to manage API usage and prevent abuse
"""

import time
import logging
from typing import Dict, DefaultDict
from collections import defaultdict, deque
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple in-memory rate limiter for bot usage"""
    
    def __init__(self):
        # User request tracking
        self.user_requests: DefaultDict[int, DefaultDict[str, deque]] = defaultdict(lambda: defaultdict(deque))
        
        # Rate limits configuration
        self.limits = {
            'text_query': {
                'max_requests': 10,
                'time_window': 3600,  # 1 hour in seconds
                'description': '10 queries per hour'
            },
            'document_analysis': {
                'max_requests': 3,
                'time_window': 86400,  # 24 hours in seconds
                'description': '3 document analyses per day'
            }
        }
    
    def check_rate_limit(self, user_id: int, request_type: str) -> bool:
        """
        Check if user has exceeded rate limit for given request type
        
        Args:
            user_id: Telegram user ID
            request_type: Type of request ('text_query' or 'document_analysis')
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        try:
            if request_type not in self.limits:
                logger.warning(f"Unknown request type: {request_type}")
                return True  # Allow unknown request types by default
            
            limit_config = self.limits[request_type]
            max_requests = limit_config['max_requests']
            time_window = limit_config['time_window']
            
            current_time = time.time()
            user_queue = self.user_requests[user_id][request_type]
            
            # Remove old requests outside the time window
            while user_queue and current_time - user_queue[0] > time_window:
                user_queue.popleft()
            
            # Check if user has exceeded the limit
            if len(user_queue) >= max_requests:
                logger.info(f"Rate limit exceeded for user {user_id}, request type: {request_type}")
                return False
            
            # Add current request to the queue
            user_queue.append(current_time)
            
            logger.debug(f"Rate limit check passed for user {user_id}, request type: {request_type} ({len(user_queue)}/{max_requests})")
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow request on error to avoid blocking users
    
    def get_remaining_requests(self, user_id: int, request_type: str) -> int:
        """Get number of remaining requests for user"""
        try:
            if request_type not in self.limits:
                return -1  # Unlimited for unknown types
            
            limit_config = self.limits[request_type]
            max_requests = limit_config['max_requests']
            time_window = limit_config['time_window']
            
            current_time = time.time()
            user_queue = self.user_requests[user_id][request_type]
            
            # Remove old requests outside the time window
            while user_queue and current_time - user_queue[0] > time_window:
                user_queue.popleft()
            
            return max(0, max_requests - len(user_queue))
            
        except Exception as e:
            logger.error(f"Error getting remaining requests: {e}")
            return 0
    
    def get_reset_time(self, user_id: int, request_type: str) -> datetime:
        """Get time when rate limit will reset for user"""
        try:
            if request_type not in self.limits:
                return datetime.now()
            
            limit_config = self.limits[request_type]
            time_window = limit_config['time_window']
            
            user_queue = self.user_requests[user_id][request_type]
            
            if not user_queue:
                return datetime.now()
            
            # Find the oldest request
            oldest_request_time = user_queue[0]
            reset_time = datetime.fromtimestamp(oldest_request_time + time_window)
            
            return reset_time
            
        except Exception as e:
            logger.error(f"Error getting reset time: {e}")
            return datetime.now()
    
    def get_user_stats(self, user_id: int) -> Dict[str, Dict]:
        """Get user's current rate limit stats"""
        stats = {}
        
        for request_type, limit_config in self.limits.items():
            remaining = self.get_remaining_requests(user_id, request_type)
            reset_time = self.get_reset_time(user_id, request_type)
            
            stats[request_type] = {
                'limit': limit_config['max_requests'],
                'remaining': remaining,
                'used': limit_config['max_requests'] - remaining,
                'reset_time': reset_time,
                'description': limit_config['description']
            }
        
        return stats
    
    def cleanup_old_data(self, max_age_hours: int = 24):
        """Clean up old rate limit data to prevent memory bloat"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            users_to_remove = []
            
            for user_id, request_types in self.user_requests.items():
                types_to_remove = []
                
                for request_type, user_queue in request_types.items():
                    # Remove old requests
                    while user_queue and current_time - user_queue[0] > max_age_seconds:
                        user_queue.popleft()
                    
                    # Mark empty queues for removal
                    if not user_queue:
                        types_to_remove.append(request_type)
                
                # Remove empty request type queues
                for request_type in types_to_remove:
                    del request_types[request_type]
                
                # Mark users with no active requests for removal
                if not request_types:
                    users_to_remove.append(user_id)
            
            # Remove users with no active requests
            for user_id in users_to_remove:
                del self.user_requests[user_id]
            
            logger.info(f"Cleaned up rate limiter data: removed {len(users_to_remove)} inactive users")
            
        except Exception as e:
            logger.error(f"Error cleaning up rate limiter data: {e}")
    
    def get_global_stats(self) -> Dict[str, int]:
        """Get global rate limiter statistics"""
        try:
            stats = {
                'total_users': len(self.user_requests),
                'active_users': 0,
                'total_requests_tracked': 0
            }
            
            current_time = time.time()
            
            for user_id, request_types in self.user_requests.items():
                user_has_recent_requests = False
                
                for request_type, user_queue in request_types.items():
                    # Count requests in the last 24 hours
                    recent_requests = sum(1 for req_time in user_queue if current_time - req_time < 86400)
                    stats['total_requests_tracked'] += recent_requests
                    
                    if recent_requests > 0:
                        user_has_recent_requests = True
                
                if user_has_recent_requests:
                    stats['active_users'] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting global stats: {e}")
            return {'total_users': 0, 'active_users': 0, 'total_requests_tracked': 0}
