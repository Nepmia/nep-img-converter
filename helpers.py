import os
import dotenv

dotenv.load_dotenv()

log_base_dir = os.getenv("LOG_BASE_DIR")

def verify_logs() -> bool:  
    """Check if log folder exists

    Returns:
        bool: If log exist 
    """
    if not os.path.exists(log_base_dir):
        return False
    return True

def create_log_folder():
    """Create the log folder
    """
    os.mkdir(log_base_dir)    