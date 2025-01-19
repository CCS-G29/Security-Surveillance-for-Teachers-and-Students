# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.utils import ldap_connection, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        conn = ldap_connection(current_app)
        
        if user_type == 'admin':
            if conn.search(f'cn={username},ou=users,{current_app.config["LDAP_BASE_DN"]}',
                         '(objectClass=*)',
                         attributes=['userPassword']):
                stored_hash = conn.entries[0].userPassword.value.decode()
                if verify_password(password, stored_hash):
                    session['user'] = username
                    session['user_type'] = 'admin'
                    return redirect(url_for('admin.dashboard'))
        
        elif user_type == 'teacher':
            if conn.search(f'cn={username},ou=users,{current_app.config["LDAP_BASE_DN"]}',
                         '(objectClass=*)',
                         attributes=['userPassword']):
                stored_hash = conn.entries[0].userPassword.value.decode()
                if verify_password(password, stored_hash):
                    session['user'] = username
                    session['user_type'] = 'teacher'
                    return redirect(url_for('teacher.dashboard'))
        
        flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
