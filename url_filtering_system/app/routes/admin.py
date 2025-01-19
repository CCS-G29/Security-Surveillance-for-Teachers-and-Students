# app/routes/admin.py

from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from app.models import URL
from app.utils import ldap_connection, hash_password, update_pfsense_acls

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']
        
        conn = ldap_connection(current_app)
        
        user_dn = f'cn={username},ou=users,{current_app.config["LDAP_BASE_DN"]}'
        
        attributes = {
            'objectClass': ['top', 'inetOrgPerson'],
            'cn': username,
            'sn': full_name,
            'userPassword': f'{{SHA}}{hash_password(password)}',
            'mail': email
        }
        
        conn.add(user_dn, attributes=attributes)
        
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_teacher.html')

@admin_bp.route('/manage-url', methods=['GET', 'POST'])
def manage_url():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        url = request.form['url']
        action = request.form['action']
        
        url_model = URL(current_app.db)
        url_model.add_url(url, action, session['user'])
        
        # Update pfSense
        urls = url_model.get_active_urls()
        blacklist = [u['url'] for u in urls if u['action'] == 'blocked']
        whitelist = [u['url'] for u in urls if u['action'] == 'allowed']
        update_pfsense_acls(current_app, blacklist, whitelist)
        
        return redirect(url_for('admin.manage_url'))
    
    return render_template('admin/manage_url.html')

@admin_bp.route('/view-history')
def view_history():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    
    url_model = URL(current_app.db)
    history = url_model.get_history()
    
    return render_template('admin/view_history.html', history=history)

@admin_bp.route('/active-urls')
def active_urls():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    
    url_model = URL(current_app.db)
    urls = url_model.get_active_urls()
    
    return render_template('admin/active_urls.html', urls=urls)
