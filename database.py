from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class WebsiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False, index=True)
    content_key = db.Column(db.String(100), nullable=False, index=True)
    content_type = db.Column(db.String(50), default='text')  # text, html, image, json
    content_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Unique constraint on section + content_key
    __table_args__ = (db.UniqueConstraint('section', 'content_key', name='uix_section_key'),)
    
    def __repr__(self):
        return f'<WebsiteContent {self.section}.{self.content_key}>'

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # image, document, other
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<UploadedFile {self.filename}>'

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PageVisit {self.page} at {self.visited_at}>'

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    is_responded = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactSubmission {self.name}>'

def init_db():
    # Create all tables
    db.create_all()
    
    # Create default admin user if not exists
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(
            username='admin',
            password_hash=hashed_password,
            email='admin@wonderlandedu.com',
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: admin / admin123")
    
    # Create default website content
    default_content = [
        # Hero Section
        ('hero', 'title', 'text', 'Unlocking Your Academic Future', 'Main hero title'),
        ('hero', 'subtitle', 'text', 'Expert guidance for international students to achieve their educational dreams. With over 15 years of experience, we\'ve helped 5000+ students secure admissions in top universities worldwide.', 'Hero subtitle'),
        ('hero', 'stat1_number', 'text', '98%', 'Success rate percentage'),
        ('hero', 'stat1_text', 'text', 'Success Rate', 'Success rate text'),
        ('hero', 'stat2_number', 'text', '5000+', 'Students helped number'),
        ('hero', 'stat2_text', 'text', 'Students Helped', 'Students helped text'),
        ('hero', 'stat3_number', 'text', '50+', 'Countries number'),
        ('hero', 'stat3_text', 'text', 'Countries', 'Countries text'),
        
        # Services Section
        ('services', 'title', 'text', 'Our Premium Services', 'Services section title'),
        ('services', 'subtitle', 'text', 'Comprehensive support for your educational journey', 'Services section subtitle'),
        
        # Service 1
        ('service1', 'title', 'text', 'University Admissions', 'Service 1 title'),
        ('service1', 'description', 'text', 'Personalized university selection, application assistance, and scholarship guidance for top institutions worldwide.', 'Service 1 description'),
        ('service1', 'feature1', 'text', 'Profile Evaluation', 'Service 1 feature 1'),
        ('service1', 'feature2', 'text', 'University Shortlisting', 'Service 1 feature 2'),
        ('service1', 'feature3', 'text', 'Application Review', 'Service 1 feature 3'),
        ('service1', 'feature4', 'text', 'Scholarship Assistance', 'Service 1 feature 4'),
        
        # Service 2
        ('service2', 'title', 'text', 'Visa Processing', 'Service 2 title'),
        ('service2', 'description', 'text', 'End-to-end visa assistance with 98% success rate. Documentation, interview preparation, and post-visa support.', 'Service 2 description'),
        ('service2', 'feature1', 'text', 'Documentation Guidance', 'Service 2 feature 1'),
        ('service2', 'feature2', 'text', 'Interview Preparation', 'Service 2 feature 2'),
        ('service2', 'feature3', 'text', 'Financial Planning', 'Service 2 feature 3'),
        ('service2', 'feature4', 'text', 'Post-Visa Support', 'Service 2 feature 4'),
        
        # Service 3
        ('service3', 'title', 'text', 'Test Preparation', 'Service 3 title'),
        ('service3', 'description', 'text', 'Expert coaching for IELTS, TOEFL, GRE, GMAT, SAT with proven strategies and mock test series.', 'Service 3 description'),
        ('service3', 'feature1', 'text', 'Custom Study Plans', 'Service 3 feature 1'),
        ('service3', 'feature2', 'text', 'Mock Tests & Analysis', 'Service 3 feature 2'),
        ('service3', 'feature3', 'text', 'One-on-One Coaching', 'Service 3 feature 3'),
        ('service3', 'feature4', 'text', 'Score Improvement', 'Service 3 feature 4'),
        
        # Testimonials
        ('testimonials', 'title', 'text', 'Student Success Stories', 'Testimonials section title'),
        ('testimonials', 'subtitle', 'text', 'Hear from our students who achieved their dreams with our guidance', 'Testimonials section subtitle'),
        
        # Testimonial 1
        ('testimonial1', 'name', 'text', 'Priya Sharma', 'Testimonial 1 name'),
        ('testimonial1', 'course', 'text', 'Computer Science, Stanford University', 'Testimonial 1 course'),
        ('testimonial1', 'text', 'text', '"Wonderland Consultancy helped me secure admission to Stanford with a 50% scholarship. Their personalized guidance and mock interviews were invaluable. I couldn\'t have done it without them!"', 'Testimonial 1 text'),
        ('testimonial1', 'admission', 'text', 'Admitted: Fall 2023', 'Testimonial 1 admission'),
        ('testimonial1', 'achievement', 'text', 'Scholarship: $40,000', 'Testimonial 1 achievement'),
        
        # Contact Information
        ('contact', 'address_line1', 'text', '123 Education Street, Knowledge City', 'Contact address line 1'),
        ('contact', 'address_line2', 'text', 'Mumbai, India - 400001', 'Contact address line 2'),
        ('contact', 'phone', 'text', '+91 98765 43210', 'Contact phone number'),
        ('contact', 'email1', 'text', 'info@wonderlandedu.com', 'Contact email 1'),
        ('contact', 'email2', 'text', 'admissions@wonderlandedu.com', 'Contact email 2'),
        ('contact', 'hours', 'text', 'Mon-Sat, 9AM-7PM', 'Contact hours'),
        
        # Footer
        ('footer', 'about', 'text', 'Empowering students to achieve their academic dreams through expert guidance and personalized support since 2008.', 'Footer about text'),
        ('footer', 'copyright', 'text', 'Wonderland Educational Consultancy Pvt. Ltd.', 'Copyright text'),
    ]
    
    for section, key, content_type, value, description in default_content:
        content = WebsiteContent.query.filter_by(section=section, content_key=key).first()
        if not content:
            content = WebsiteContent(
                section=section,
                content_key=key,
                content_type=content_type,
                content_value=value,
                description=description
            )
            db.session.add(content)
    
    try:
        db.session.commit()
        print("Default website content created")
    except:
        db.session.rollback()