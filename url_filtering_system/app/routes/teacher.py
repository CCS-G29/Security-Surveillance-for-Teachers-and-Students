# app/routes/teacher.py
from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from app.models import URL
from app.utils import update_pfsense_acls

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
def dashboard():
    if session.get('user_type') != 'teacher':
        return redirect(url_for('auth.login'))
    return render_template('teacher/dashboard.html')

@teacher_bp.route('/manage-url', methods=['GET', 'POST'])
def manage_url():
    if session.get('user_type') != 'teacher':
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
        
        return redirect(url_for('teacher.manage_url'))
    
    return render_template('teacher/manage_url.html')

@teacher_bp.route('/view-history')
def view_history():
    if session.get('user_type') != 'teacher':
        return redirect(url_for('auth.login'))
    
    url_model = URL(current_app.db)
    history = url_model.get_history(session['user'])
    
    return render_template('teacher/view_history.html', history=history)