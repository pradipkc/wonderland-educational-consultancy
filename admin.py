from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import json
from PIL import Image
import uuid
from datetime import datetime

from config import Config
from database import db, User, WebsiteContent, UploadedFile, PageVisit, ContactSubmission
from models import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_file(file, file_type='other'):
    if file and allowed_file(file.filename):
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        
        # Determine upload path
        if file_type == 'image':
            upload_path = os.path.join(Config.UPLOAD_FOLDER, 'images')
        else:
            upload_path = os.path.join(Config.UPLOAD_FOLDER, 'files')
        
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create database record
        uploaded_file = UploadedFile(
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_type,
            file_path=file_path,
            file_size=file_size,
            uploaded_by=current_user.id
        )
        
        db.session.add(uploaded_file)
        db.session.commit()
        
        return uploaded_file
    
    return None

def resize_image(image_path, max_size=(1200, 800)):
    """Resize image to optimize for web"""
    try:
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False

# Admin Routes
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_visits = PageVisit.query.count()
    total_contacts = ContactSubmission.query.count()
    total_files = UploadedFile.query.count()
    unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
    
    # Recent activity
    recent_contacts = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).limit(5).all()
    recent_visits = PageVisit.query.order_by(PageVisit.visited_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_visits=total_visits,
                         total_contacts=total_contacts,
                         total_files=total_files,
                         unread_contacts=unread_contacts,
                         recent_contacts=recent_contacts,
                         recent_visits=recent_visits)

@admin_bp.route('/content')
@login_required
def content_management():
    sections = db.session.query(WebsiteContent.section).distinct().all()
    sections = [s[0] for s in sections]
    
    # Get all content grouped by section
    content_by_section = {}
    for section in sections:
        content_items = WebsiteContent.query.filter_by(section=section).all()
        content_by_section[section] = content_items
    
    return render_template('admin/edit_content.html',
                         sections=sections,
                         content_by_section=content_by_section)

@admin_bp.route('/content/update', methods=['POST'])
@login_required
def update_content():
    try:
        data = request.get_json()
        section = data.get('section')
        content_key = data.get('key')
        content_value = data.get('value')
        
        if not all([section, content_key, content_value is not None]):
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        # Find or create content
        content = WebsiteContent.query.filter_by(
            section=section,
            content_key=content_key
        ).first()
        
        if not content:
            content = WebsiteContent(
                section=section,
                content_key=content_key,
                content_type='text'
            )
        
        content.content_value = content_value
        content.updated_by = current_user.id
        
        db.session.add(content)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Content updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@admin_bp.route('/content/add-section', methods=['POST'])
@login_required
def add_section():
    try:
        section_name = request.form.get('section_name')
        
        if not section_name:
            flash('Section name is required', 'error')
            return redirect(url_for('admin.content_management'))
        
        # Check if section exists
        existing = WebsiteContent.query.filter_by(section=section_name).first()
        if existing:
            flash('Section already exists', 'error')
            return redirect(url_for('admin.content_management'))
        
        # Create a sample content item
        content = WebsiteContent(
            section=section_name,
            content_key='title',
            content_type='text',
            content_value='New Section Title',
            description='Title for the new section'
        )
        
        db.session.add(content)
        db.session.commit()
        
        flash('Section added successfully!', 'success')
        return redirect(url_for('admin.content_management'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding section: {str(e)}', 'error')
        return redirect(url_for('admin.content_management'))

@admin_bp.route('/uploads')
@login_required
def file_manager():
    files = UploadedFile.query.order_by(UploadedFile.uploaded_at.desc()).all()
    return render_template('admin/uploads.html', files=files)

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('admin.file_manager'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin.file_manager'))
    
    # Determine file type
    if file.content_type.startswith('image/'):
        file_type = 'image'
    else:
        file_type = 'other'
    
    uploaded_file = save_file(file, file_type)
    
    if uploaded_file:
        # Resize if image
        if file_type == 'image':
            resize_image(uploaded_file.file_path)
        
        flash('File uploaded successfully!', 'success')
    else:
        flash('Invalid file type', 'error')
    
    return redirect(url_for('admin.file_manager'))

@admin_bp.route('/delete-file/<int:file_id>')
@login_required
def delete_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)
    
    # Delete physical file
    try:
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
    except:
        pass
    
    # Delete database record
    db.session.delete(file)
    db.session.commit()
    
    flash('File deleted successfully!', 'success')
    return redirect(url_for('admin.file_manager'))

@admin_bp.route('/contacts')
@login_required
def contact_submissions():
    submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
    return render_template('admin/contacts.html', submissions=submissions)

@admin_bp.route('/contact/<int:contact_id>/read')
@login_required
def mark_contact_read(contact_id):
    submission = ContactSubmission.query.get_or_404(contact_id)
    submission.is_read = True
    db.session.commit()
    
    flash('Marked as read', 'success')
    return redirect(url_for('admin.contact_submissions'))

@admin_bp.route('/contact/<int:contact_id>/delete')
@login_required
def delete_contact(contact_id):
    submission = ContactSubmission.query.get_or_404(contact_id)
    db.session.delete(submission)
    db.session.commit()
    
    flash('Contact submission deleted', 'success')
    return redirect(url_for('admin.contact_submissions'))

@admin_bp.route('/analytics')
@login_required
def analytics():
    # Get page visit statistics
    page_stats = db.session.query(
        PageVisit.page,
        db.func.count(PageVisit.id).label('visits')
    ).group_by(PageVisit.page).all()
    
    # Get daily visits for last 7 days
    import datetime
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    
    daily_stats = db.session.query(
        db.func.date(PageVisit.visited_at).label('date'),
        db.func.count(PageVisit.id).label('visits')
    ).filter(PageVisit.visited_at >= seven_days_ago)\
     .group_by(db.func.date(PageVisit.visited_at))\
     .order_by(db.func.date(PageVisit.visited_at)).all()
    
    return render_template('admin/analytics.html',
                         page_stats=page_stats,
                         daily_stats=daily_stats)

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/api/get-content')
def get_content_api():
    """API endpoint for frontend to fetch content"""
    section = request.args.get('section')
    
    if section:
        content_items = WebsiteContent.query.filter_by(section=section).all()
    else:
        content_items = WebsiteContent.query.all()
    
    content_dict = {}
    for item in content_items:
        if item.section not in content_dict:
            content_dict[item.section] = {}
        content_dict[item.section][item.content_key] = item.content_value
    
    return jsonify(content_dict)

@admin_bp.route('/api/get-image/<path:filename>')
def get_image(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)