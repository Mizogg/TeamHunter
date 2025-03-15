"""
Logger module for TeamHunter
Provides logging functionality for the application
"""
import os
import logging
import datetime
from pathlib import Path

class TeamHunterLogger:
    """
    Logger class for TeamHunter application
    """
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create a unique log file name with current timestamp
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"teamhunter_{timestamp}.log")
        
        # Configure the logger
        self.logger = logging.getLogger("TeamHunter")
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger initialized. Log file: {self.log_file}")
        
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
        
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
        
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
        
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
        
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message)
        
    def exception(self, message):
        """Log an exception message with traceback"""
        self.logger.exception(message)
        
    def get_log_file_path(self):
        """Get the path to the current log file"""
        return self.log_file
        
    def get_all_logs(self):
        """Get a list of all log files"""
        return [os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir) if f.endswith('.log')]
        
    def clear_old_logs(self, days=7):
        """Clear log files older than specified days"""
        now = datetime.datetime.now()
        count = 0
        
        for log_file in self.get_all_logs():
            try:
                # Extract timestamp from filename (format: teamhunter_YYYYMMDD_HHMMSS.log)
                filename = os.path.basename(log_file)
                if not filename.startswith('teamhunter_'):
                    continue
                    
                date_str = filename.split('_')[1]  # Get YYYYMMDD part
                if len(date_str) != 8:  # Basic validation
                    continue
                    
                file_date = datetime.datetime.strptime(date_str, '%Y%m%d')
                if (now - file_date).days > days and log_file != self.log_file:  # Don't delete current log
                    try:
                        os.remove(log_file)
                        count += 1
                        self.info(f"Removed old log file: {filename}")
                    except Exception as e:
                        self.error(f"Failed to remove old log file {log_file}: {e}")
            except Exception as e:
                self.error(f"Error processing log file {log_file}: {e}")
                    
        self.info(f"Cleared {count} log files older than {days} days")
        return count
        
# Create a singleton instance
logger = TeamHunterLogger() 