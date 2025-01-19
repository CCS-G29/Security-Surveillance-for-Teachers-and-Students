# app/routes/urls.py

from flask import jsonify, request, render_template, Blueprint
from app.models import URL
from app.utils import update_pfsense_acls, clean_url
import logging

url_bp = Blueprint('url', __name__)

@url_bp.route('/')
def index():
    return render_template('index.html')

@url_bp.route('/api/urls', methods=['GET'])
def get_urls():
    """Get current blacklist and whitelist"""
    try:
        if app.mongo_client is None:
            raise Exception("MongoDB not connected")
        urls = app.urls_collection.find_one({}, {'_id': 0}) or {'blacklist': [], 'whitelist': []}
        return jsonify(urls)
    except Exception as e:
        logging.error(f"Error getting URLs: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@url_bp.route('/api/urls', methods=['POST'])
def update_urls():
    """Update URL lists"""
    try:
        if app.mongo_client is None:
            raise Exception("MongoDB not connected")
        
        data = request.json
        blacklist = data.get('blacklist', [])
        whitelist = data.get('whitelist', [])
        
        # Clean URLs
        cleaned_blacklist = [clean_url(url) for url in blacklist]
        cleaned_whitelist = [clean_url(url) for url in whitelist]
        
        # Update MongoDB with cleaned URLs
        app.urls_collection.replace_one({}, {
            'blacklist': cleaned_blacklist,
            'whitelist': cleaned_whitelist
        }, upsert=True)
        
        # Update pfSense with cleaned URLs
        update_pfsense_acls(app, cleaned_blacklist, cleaned_whitelist)
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error updating URLs: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500