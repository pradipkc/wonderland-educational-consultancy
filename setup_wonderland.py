# setup_wonderland.py
import os

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'static/uploads',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True

def create_app_py():
    """Create the main app.py file"""
    app_content = '''from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wonderland.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WebsiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    content_key = db.Column(db.String(100), nullable=False)
    content_value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    # Using SQLAlchemy 2.0 compatible syntax
    return db.session.get(User, int(user_id))

# Initialize database
def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        admin_user = db.session.execute(
            db.select(User).filter_by(username='admin')
        ).scalar_one_or_none()
        
        if not admin_user:
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(
                username='admin',
                password_hash=hashed_password,
                is_admin=True
            )
            db.session.add(admin_user)
            print("✓ Default admin user created: admin / admin123")
        
        # Create default website content
        default_content = [
            # Hero Section
            ('hero', 'title', 'Unlocking Your Academic Future'),
            ('hero', 'subtitle', 'Expert guidance for international students to achieve their educational dreams. With over 15 years of experience, we\'ve helped 5000+ students secure admissions in top universities worldwide.'),
            ('hero', 'stat1_number', '98%'),
            ('hero', 'stat1_text', 'Success Rate'),
            ('hero', 'stat2_number', '5000+'),
            ('hero', 'stat2_text', 'Students Helped'),
            ('hero', 'stat3_number', '50+'),
            ('hero', 'stat3_text', 'Countries'),
            
            # Services Section
            ('services', 'title', 'Our Premium Services'),
            ('services', 'subtitle', 'Comprehensive support for your educational journey'),
            
            # Service 1
            ('service1', 'title', 'University Admissions'),
            ('service1', 'description', 'Personalized university selection, application assistance, and scholarship guidance for top institutions worldwide.'),
            ('service1', 'feature1', 'Profile Evaluation'),
            ('service1', 'feature2', 'University Shortlisting'),
            ('service1', 'feature3', 'Application Review'),
            ('service1', 'feature4', 'Scholarship Assistance'),
            
            # Service 2
            ('service2', 'title', 'Visa Processing'),
            ('service2', 'description', 'End-to-end visa assistance with 98% success rate. Documentation, interview preparation, and post-visa support.'),
            ('service2', 'feature1', 'Documentation Guidance'),
            ('service2', 'feature2', 'Interview Preparation'),
            ('service2', 'feature3', 'Financial Planning'),
            ('service2', 'feature4', 'Post-Visa Support'),
            
            # Service 3
            ('service3', 'title', 'Test Preparation'),
            ('service3', 'description', 'Expert coaching for IELTS, TOEFL, GRE, GMAT, SAT with proven strategies and mock test series.'),
            ('service3', 'feature1', 'Custom Study Plans'),
            ('service3', 'feature2', 'Mock Tests & Analysis'),
            ('service3', 'feature3', 'One-on-One Coaching'),
            ('service3', 'feature4', 'Score Improvement'),
            
            # Testimonials
            ('testimonials', 'title', 'Student Success Stories'),
            ('testimonials', 'subtitle', 'Hear from our students who achieved their dreams with our guidance'),
            
            # Testimonial 1
            ('testimonial1', 'name', 'Priya Sharma'),
            ('testimonial1', 'course', 'Computer Science, Stanford University'),
            ('testimonial1', 'text', '"Wonderland Consultancy helped me secure admission to Stanford with a 50% scholarship. Their personalized guidance and mock interviews were invaluable. I couldn\'t have done it without them!"'),
            ('testimonial1', 'admission', 'Admitted: Fall 2023'),
            ('testimonial1', 'achievement', 'Scholarship: $40,000'),
            
            # Contact Information
            ('contact', 'address_line1', '123 Education Street, Knowledge City'),
            ('contact', 'address_line2', 'Mumbai, India - 400001'),
            ('contact', 'phone', '+91 98765 43210'),
            ('contact', 'email1', 'info@wonderlandedu.com'),
            ('contact', 'email2', 'admissions@wonderlandedu.com'),
            ('contact', 'hours', 'Mon-Sat, 9AM-7PM'),
            
            # Footer
            ('footer', 'about', 'Empowering students to achieve their academic dreams through expert guidance and personalized support since 2008.'),
            ('footer', 'copyright', 'Wonderland Educational Consultancy Pvt. Ltd.'),
        ]
        
        # Add default content if not exists
        for section, key, value in default_content:
            existing = db.session.execute(
                db.select(WebsiteContent).filter_by(section=section, content_key=key)
            ).scalar_one_or_none()
            
            if not existing:
                content = WebsiteContent(
                    section=section,
                    content_key=key,
                    content_value=value
                )
                db.session.add(content)
        
        try:
            db.session.commit()
            print("✓ Default website content created")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating default content: {e}")

# Frontend Routes
@app.route('/')
def index():
    # Fetch all content from database
    content_items = db.session.execute(
        db.select(WebsiteContent)
    ).scalars().all()
    
    # Organize content by section
    content_dict = {}
    for item in content_items:
        if item.section not in content_dict:
            content_dict[item.section] = {}
        content_dict[item.section][item.content_key] = item.content_value
    
    # Debug: print what content we have
    print(f"Loaded {len(content_items)} content items from database")
    for section, items in content_dict.items():
        print(f"Section: {section} - Items: {list(items.keys())}")
    
    return render_template('index.html', content=content_dict)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        service = data.get('service')
        message = data.get('message')
        
        # Save to database
        submission = ContactSubmission(
            name=name,
            email=email,
            phone=phone,
            service=service,
            message=message
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thank you for contacting Wonderland Educational Consultancy! We will get back to you within 24 hours.'
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'message': 'There was an error. Please try again.'
        }), 500

@app.route('/book_consultation', methods=['POST'])
def book_consultation():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        service = data.get('service')
        date = data.get('date')
        
        # Save as contact submission
        submission = ContactSubmission(
            name=name,
            email=email,
            service=f"Consultation Booking: {service}",
            message=f"Requested consultation for {date}"
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Your consultation has been booked successfully! Check your email for confirmation.'
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'message': 'There was an error. Please try again.'
        }), 500

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Use SQLAlchemy 2.0 syntax
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/content/editor')
@login_required
def admin_content_editor():
    # Get all content grouped by section
    content_items = db.session.execute(
        db.select(WebsiteContent).order_by(WebsiteContent.section, WebsiteContent.content_key)
    ).scalars().all()
    
    # Organize by section
    sections = {}
    for item in content_items:
        if item.section not in sections:
            sections[item.section] = []
        sections[item.section].append(item)
    
    return render_template('admin_content_editor.html', sections=sections)

@app.route('/admin/content/update', methods=['POST'])
@login_required
def update_content():
    try:
        data = request.get_json()
        section = data.get('section')
        content_key = data.get('key')
        content_value = data.get('value')
        
        # Find existing content
        content = db.session.execute(
            db.select(WebsiteContent).filter_by(section=section, content_key=content_key)
        ).scalar_one_or_none()
        
        if content:
            # Update existing
            content.content_value = content_value
        else:
            # Create new
            content = WebsiteContent(
                section=section,
                content_key=content_key,
                content_value=content_value
            )
            db.session.add(content)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Content updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    # Use SQLAlchemy 2.0 syntax
    submissions = db.session.execute(
        db.select(ContactSubmission).order_by(ContactSubmission.submitted_at.desc())
    ).scalars().all()
    
    return render_template('admin_contacts.html', submissions=submissions)

# Static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    init_db()
    print("\\n" + "="*50)
    print("WONDERLAND EDUCATIONAL CONSULTANCY")
    print("="*50)
    print("🌐 Website: http://localhost:5000")
    print("🔐 Admin Login: http://localhost:5000/admin/login")
    print("👤 Username: admin")
    print("🔑 Password: admin123")
    print("="*50)
    print("\\n📢 Server is running... Press Ctrl+C to stop\\n")
    app.run(debug=True, port=5000)
'''
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("✓ Created app.py")

def create_admin_templates():
    """Create admin template files"""
    
    # admin_login.html
    login_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Wonderland Educational Consultancy</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        .login-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .login-header {
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
            color: white;
            border-radius: 15px 15px 0 0;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="login-card">
                    <div class="login-header text-center">
                        <h2><i class="fas fa-crown"></i> Wonderland Admin</h2>
                        <p class="mb-0">Sign in to manage your website</p>
                    </div>
                    <div class="card-body p-4">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% if messages %}
                                {% for category, message in messages %}
                                    <div class="alert alert-{{ category }} alert-dismissible fade show">
                                        {{ message }}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                    </div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}
                        
                        <form method="POST" action="{{ url_for('admin_login') }}">
                            <div class="mb-3">
                                <label for="username" class="form-label">
                                    <i class="fas fa-user"></i> Username
                                </label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">
                                    <i class="fas fa-lock"></i> Password
                                </label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-sign-in-alt"></i> Login
                                </button>
                            </div>
                        </form>
                        <div class="text-center mt-3">
                            <small class="text-muted">Default: admin / admin123</small>
                        </div>
                        <div class="text-center mt-4">
                            <a href="/" class="text-decoration-none">
                                <i class="fas fa-arrow-left"></i> Back to Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    with open('templates/admin_login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    print("✓ Created templates/admin_login.html")
    
    # admin_content_editor.html (simplified version)
    editor_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Editor - Wonderland Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f5f7fb; padding: 20px; }
        .content-section { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
        .content-item { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
        .content-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1><i class="fas fa-edit text-primary"></i> Edit Website Content</h1>
            <div>
                <a href="{{ url_for('admin_dashboard') }}" class="btn btn-secondary">Back to Dashboard</a>
                <a href="/" target="_blank" class="btn btn-info">View Site</a>
                <a href="{{ url_for('admin_logout') }}" class="btn btn-danger">Logout</a>
            </div>
        </div>
        
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> Edit any content below. Changes are saved automatically.
        </div>
        
        <div id="contentSections">
            {% for section_name, items in sections.items() %}
            <div class="content-section">
                <h4 class="mb-3 text-primary">{{ section_name|title }}</h4>
                
                {% for item in items %}
                <div class="content-item">
                    <label class="form-label fw-bold">{{ item.content_key|replace('_', ' ')|title }}</label>
                    <textarea class="form-control content-input" 
                              data-section="{{ item.section }}"
                              data-key="{{ item.content_key }}"
                              rows="{% if item.content_key in ['description', 'text', 'about', 'subtitle'] %}3{% else %}1{% endif %}"
                              placeholder="Enter content...">{{ item.content_value }}</textarea>
                    <div class="mt-1 text-muted small">
                        Last updated: {{ item.updated_at.strftime('%Y-%m-%d %H:%M') if item.updated_at else 'Never' }}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('.content-input').on('change blur', function() {
                const $input = $(this);
                const section = $input.data('section');
                const key = $input.data('key');
                const value = $input.val();
                
                updateContent(section, key, value);
            });
        });
        
        function updateContent(section, key, value) {
            $.ajax({
                url: "{{ url_for('update_content') }}",
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    section: section,
                    key: key,
                    value: value
                }),
                success: function(response) {
                    if (response.success) {
                        showToast('✓ Content updated!');
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function() {
                    alert('Network error. Please try again.');
                }
            });
        }
        
        function showToast(message) {
            // Simple toast notification
            const toast = $('<div class="alert alert-success alert-dismissible fade show position-fixed" style="top:20px;right:20px;z-index:1000;">' + 
                           '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                           message + '</div>');
            $('body').append(toast);
            setTimeout(() => toast.remove(), 3000);
        }
    </script>
</body>
</html>'''
    
    with open('templates/admin_content_editor.html', 'w', encoding='utf-8') as f:
        f.write(editor_html)
    print("✓ Created templates/admin_content_editor.html")

def create_requirements():
    """Create requirements.txt"""
    requirements = '''Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Bcrypt==1.0.1
WTForms==3.1.1
python-dotenv==1.0.0
Pillow==10.2.0
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("✓ Created requirements.txt")

def update_index_html():
    """Update index.html with dynamic content placeholders"""
    print("⚠️  Note: You need to manually update your index.html file")
    print("Replace static text with dynamic placeholders like:")
    print("{{ content.hero.title if content and content.hero and content.hero.title else 'Default Text' }}")
    print("\nKey sections to update:")
    print("1. Hero section title and subtitle")
    print("2. Statistics numbers and text")
    print("3. Services titles and descriptions")
    print("4. Contact information")

def main():
    print("="*60)
    print("WONDERLAND EDUCATIONAL CONSULTANCY - SETUP")
    print("="*60)
    
    # Create directory structure
    create_directory_structure()
    
    # Create app.py
    create_app_py()
    
    # Create admin templates
    create_admin_templates()
    
    # Create requirements.txt
    create_requirements()
    
    # Instructions for index.html
    update_index_html()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Update your index.html with dynamic content placeholders")
    print("3. Run the server: python app.py")
    print("4. Visit: http://localhost:5000")
    print("5. Admin login: http://localhost:5000/admin/login")
    print("   Username: admin")
    print("   Password: admin123")
    print("\nFor dynamic content, replace static text in index.html with:")
    print("{{ content.section.key if content and content.section and content.section.key else 'Default' }}")
    print("="*60)

if __name__ == '__main__':
    main()