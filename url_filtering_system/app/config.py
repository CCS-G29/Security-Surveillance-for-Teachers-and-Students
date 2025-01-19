import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # MongoDB settings for the deployed instance
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB = os.getenv('MONGO_DB', 'url_manager_system')
    
    # LDAP settings for production use
    LDAP_SERVER = os.getenv('LDAP_SERVER')
    LDAP_USER = os.getenv('LDAP_USER')
    LDAP_PASSWORD = os.getenv('LDAP_PASSWORD')
    LDAP_BASE_DN = os.getenv('LDAP_BASE_DN')
    
    # pfSense settings (firewall access)
    PFSENSE_HOST = os.getenv('PFSENSE_HOST')
    PFSENSE_USER = os.getenv('PFSENSE_USER')
    PFSENSE_PASSWORD = os.getenv('PFSENSE_PASSWORD')
