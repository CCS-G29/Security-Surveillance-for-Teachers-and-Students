# app/utils.py
import hashlib
import logging
from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_ADD
import paramiko


def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    return sha256_hash.hexdigest()

def verify_password(entered_password, stored_hash):
    entered_hash = hash_password(entered_password)
    return entered_hash == stored_hash.replace('{SHA}', '')

def ldap_connection(config):
    server = Server(config['LDAP_SERVER'], get_info=ALL)
    conn = Connection(server, 
                     user=config['LDAP_USER'],
                     password=config['LDAP_PASSWORD'],
                     auto_bind=True)
    return conn

def ssh_connect(config):
    """Establish SSH connection to pfSense with error handling"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            config['PFSENSE_HOST'],
            username=config['PFSENSE_USER'],
            password=config['PFSENSE_PASSWORD'],
            timeout=5
        )
        logging.info("Successfully connected to pfSense via SSH")
        return ssh
    except Exception as e:
        logging.error(f"SSH connection error: {str(e)}")
        raise

def update_pfsense_acls(config, blacklist, whitelist):
    """Update pfSense ACLs with improved error handling and domain management"""
    try:
        ssh = ssh_connect(config)
        
        # First read existing blacklist from pfSense's file
        stdin, stdout, stderr = ssh.exec_command('cat /var/squid/acl/blacklist.acl')
        existing_domains = set(stdout.read().decode().strip().split('\n'))
        # Remove any empty strings
        existing_domains = {domain for domain in existing_domains if domain}
        
        # Add new domains to the existing set
        for url in blacklist:
            domain = url.strip().lower()
            existing_domains.add(domain)
            if not domain.startswith('www.'):
                existing_domains.add('www.' + domain)
                
        # Create content with all domains
        blacklist_content = "\n".join(sorted(existing_domains))
        
        # Write back to pfSense ACL file
        blacklist_file = '/var/squid/acl/blacklist.acl'
        
        # Create directory if it doesn't exist
        ssh.exec_command('mkdir -p /var/squid/acl')
        
        # Write combined blacklist
        command = f'echo "{blacklist_content}" > {blacklist_file}'
        stdin, stdout, stderr = ssh.exec_command(command)
        error = stderr.read().decode().strip()
        if error:
            logging.error(f"Error writing blacklist: {error}")
            raise Exception(error)
            
        # Set permissions
        ssh.exec_command('chown -R squid:proxy /var/squid/acl')
        ssh.exec_command('chmod 644 /var/squid/acl/blacklist.acl')
        
        # Restart Squid to apply changes
        ssh.exec_command('/usr/local/etc/rc.d/squid.sh stop')
        ssh.exec_command('sleep 3')
        ssh.exec_command('/usr/local/etc/rc.d/squid.sh start')
        
        logging.info(f"Successfully updated ACLs. Total domains blocked: {len(existing_domains)}")
        
        ssh.close()
        return True
        
    except Exception as e:
        logging.error(f"Error updating pfSense ACLs: {str(e)}")
        raise

def clean_url(url):
    """Clean URLs by removing http://, https://, www. and trailing slashes"""
    cleaned_url = url.lower().replace('http://', '').replace('https://', '').replace('www.', '')
    return cleaned_url.split('/')[0]