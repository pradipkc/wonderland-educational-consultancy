from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
import os
import json
from datetime import datetime
from pymongo import MongoClient

# Initialize the Flask app correctly
app = Flask(_name_)

# Use Environment Variable for security (Follow the Render steps below)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://admin:WONDERLAND123@wonderland-cluster.vppw01v.mongodb.net/?appName=wonderland-Cluster")

client = MongoClient(MONGO_URI)
db = client["wonderland_db"]
collection = db["inquiries"]

# Your routes and logic go here...

if _name_ == "_main_":
    # Render uses the 'PORT' environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
app = Flask(__name__)
app.secret_key = 'wonderland-secret-key-2024'

# File-based storage for website content
CONTENT_FILE = 'website_content.json'

# Default website content
DEFAULT_CONTENT = {
    "hero": {
        "title": "Unlocking Your Academic Future",
        "subtitle": "Expert guidance for international students to achieve their educational dreams. With over 15 years of experience, we've helped 5000+ students secure admissions in top universities worldwide.",
        "stat1_number": "98%",
        "stat1_text": "Success Rate",
        "stat2_number": "5000+",
        "stat2_text": "Students Helped",
        "stat3_number": "50+",
        "stat3_text": "Countries"
    },
    "services": {
        "title": "Our Premium Services",
        "subtitle": "Comprehensive support for your educational journey",
        "service1": {
            "title": "University Admissions",
            "description": "Personalized university selection, application assistance, and scholarship guidance for top institutions worldwide.",
            "features": ["Profile Evaluation", "University Shortlisting", "Application Review", "Scholarship Assistance"]
        },
        "service2": {
            "title": "Visa Processing",
            "description": "End-to-end visa assistance with 98% success rate. Documentation, interview preparation, and post-visa support.",
            "features": ["Documentation Guidance", "Interview Preparation", "Financial Planning", "Post-Visa Support"]
        },
        "service3": {
            "title": "Test Preparation",
            "description": "Expert coaching for IELTS, TOEFL, GRE, GMAT, SAT with proven strategies and mock test series.",
            "features": ["Custom Study Plans", "Mock Tests & Analysis", "One-on-One Coaching", "Score Improvement"]
        }
    },
    "testimonials": {
        "title": "Student Success Stories",
        "subtitle": "Hear from our students who achieved their dreams with our guidance",
        "testimonial1": {
            "name": "Priya Sharma",
            "course": "Computer Science, Stanford University",
            "text": "Wonderland Consultancy helped me secure admission to Stanford with a 50% scholarship. Their personalized guidance and mock interviews were invaluable.",
            "admission": "Admitted: Fall 2023",
            "achievement": "Scholarship: $40,000"
        },
        "testimonial2": {
            "name": "Rahul Verma",
            "course": "Medicine, University of Oxford",
            "text": "The visa processing support was exceptional. They guided me through every document and prepared me for the interview. Got my UK student visa in just 2 weeks!",
            "admission": "Admitted: Spring 2024",
            "achievement": "Visa: UK Tier 4"
        },
        "testimonial3": {
            "name": "Anjali Patel",
            "course": "MBA, Harvard Business School",
            "text": "From GMAT preparation to interview coaching, Wonderland provided end-to-end support. Their alumni network helped me connect with current students at HBS.",
            "admission": "Admitted: Fall 2024",
            "achievement": "GMAT: 750"
        },
        "testimonial4": {
            "name": "Karthik Reddy",
            "course": "Engineering, MIT",
            "text": "I improved my IELTS score from 6.5 to 8.0 with their test prep program. The personalized study plan and regular mock tests made all the difference.",
            "admission": "Admitted: Fall 2023",
            "achievement": "IELTS: 8.0"
        },
        "testimonial5": {
            "name": "Meera Nair",
            "course": "PhD, University of Toronto",
            "text": "Wonderland helped me craft a compelling research proposal and connect with potential supervisors. Got full funding for my PhD in Canada!",
            "admission": "Admitted: Fall 2024",
            "achievement": "Funding: Full Scholarship"
        }
    },
    "partners": {
        "title": "Our Partner Universities",
        "subtitle": "Trusted by prestigious institutions worldwide",
        "region1": {
            "name": "North America",
            "universities": "University of Toronto, MIT, Stanford, Harvard"
        },
        "region2": {
            "name": "Europe",
            "universities": "University of Oxford, ETH Zurich, TU Delft"
        },
        "region3": {
            "name": "Australia/NZ",
            "universities": "University of Melbourne, ANU, University of Auckland"
        },
        "region4": {
            "name": "Asia",
            "universities": "NUS, University of Tokyo, HKU, IITs"
        }
    },
    "about": {
        "title": "About Wonderland Educational Consultancy",
        "description": "Founded in 2008, Wonderland Educational Consultancy has been transforming students' lives by guiding them towards their dream universities and careers. Our team of experienced counselors, former admission officers, and visa experts provides personalized support at every step.",
        "feature1": "Expert Counselors",
        "feature1_desc": "Former admission officers from top universities",
        "feature2": "Personalized Approach",
        "feature2_desc": "Customized strategies for each student",
        "feature3": "Ethical Practices",
        "feature3_desc": "Transparent processes, no false promises"
    },
    "contact": {
        "title": "Get In Touch",
        "subtitle": "Ready to start your educational journey? Contact us for a free consultation.",
        "address_line1": "123 Education Street, Knowledge City",
        "address_line2": "Mumbai, India - 400001",
        "phone": "+91 98765 43210",
        "hours": "Mon-Sat, 9AM-7PM",
        "email1": "info@wonderlandedu.com",
        "email2": "admissions@wonderlandedu.com"
    },
    "footer": {
        "about": "Empowering students to achieve their academic dreams through expert guidance and personalized support since 2008.",
        "copyright": "Wonderland Educational Consultancy Pvt. Ltd."
    }
}

# Simple in-memory storage for form submissions
contacts_data = []
consultations_data = []
newsletter_subscribers = []

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# ---------- CONTENT MANAGEMENT FUNCTIONS ----------


def load_content():
    """Load website content from JSON file"""
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_CONTENT.copy()
    else:
        # Create default content file
        save_content(DEFAULT_CONTENT.copy())
        return DEFAULT_CONTENT.copy()


def save_content(content):
    """Save website content to JSON file"""
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

# ---------- MAIN WEBSITE ROUTES ----------


@app.route('/')
def index():
    content = load_content()
    return render_template('index.html', content=content)


@app.route('/api/form', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        contact = {
            'id': len(contacts_data) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'service': data.get('service'),
            'message': data.get('message'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'new'
        }
        contacts_data.append(contact)
        return jsonify({'success': True, 'message': 'Thank you! We will contact you within 24 hours.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error submitting form.'}), 500


@app.route('/book_consultation', methods=['POST'])
def book_consultation():
    try:
        data = request.json
        consultation = {
            'id': len(consultations_data) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'service': data.get('service'),
            'date': data.get('date'),
            'time': data.get('time', 'Not specified'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'pending'
        }
        consultations_data.append(consultation)
        return jsonify({'success': True, 'message': 'Consultation booked successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error booking consultation.'}), 500


@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.json
        email = data.get('email')

        # Validate email
        if not email or '@' not in email:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address.'
            }), 400

        # Check if already subscribed
        if any(sub['email'] == email for sub in newsletter_subscribers):
            return jsonify({
                'success': False,
                'message': 'This email is already subscribed!'
            })

        # Create new subscriber
        subscriber = {
            'id': len(newsletter_subscribers) + 1,
            'email': email,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Add to list
        newsletter_subscribers.append(subscriber)

        # Print confirmation (for debugging)
        print(f"✓ New subscriber added: {email}")
        print(f"Total subscribers now: {len(newsletter_subscribers)}")

        return jsonify({
            'success': True,
            'message': 'Thank you for subscribing to our newsletter!'
        })

    except Exception as e:
        print(f"✗ Newsletter error: {e}")
        return jsonify({
            'success': False,
            'message': 'Subscription failed. Please try again.'
        }), 500

# ---------- ADMIN PANEL ROUTES ----------


def check_admin():
    return session.get('admin_logged_in', False)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if not check_admin():
        return redirect(url_for('admin_login'))

    # ADD THIS ONE LINE - Load content for the dashboard
    content = load_content()

    stats = {
        'total_contacts': len(contacts_data),
        'total_consultations': len(consultations_data),
        'total_subscribers': len(newsletter_subscribers),
        'new_contacts': len([c for c in contacts_data if c['status'] == 'new']),
        'pending_consultations': len([c for c in consultations_data if c['status'] == 'pending'])
    }

    return render_template('admin_dashboard.html',
                           stats=stats,
                           content=content,  # ADD THIS - pass content to template
                           recent_contacts=contacts_data[-5:][::-
                                                              1] if contacts_data else [],
                           now=datetime.now())


@app.route('/admin/content/')
def admin_content():
    if not check_admin():
        return redirect(url_for('admin_login'))
    content = load_content()
    return render_template('admin_content_editor.html', content=content)


@app.route('/admin/content/update', methods=['POST'])
def admin_content_update():
    if not check_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    try:
        data = request.json
        current_content = load_content()

        # Update nested content
        section = data.get('section')
        field = data.get('field')
        value = data.get('value')
        index = data.get('index')

        if index is not None:
            current_content[section][field][index] = value
        elif field:
            current_content[section][field] = value
        else:
            current_content[section] = value

        save_content(current_content)
        return jsonify({'success': True, 'message': 'Content updated successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/contacts')
def admin_contacts():
    if not check_admin():
        return redirect(url_for('admin_login'))
    return render_template('admin_contacts.html', contacts=contacts_data)


@app.route('/admin/consultations')
def admin_consultations():
    if not check_admin():
        return redirect(url_for('admin_login'))
    return render_template('admin_consultations.html', consultations=consultations_data)


@app.route('/admin/subscribers')
def admin_subscribers():
    if not check_admin():
        return redirect(url_for('admin_login'))

    # Print for debugging
    print(
        f"Loading subscribers page. Total subscribers: {len(newsletter_subscribers)}")

    return render_template('admin_subscribers.html', subscribers=newsletter_subscribers)


@app.route('/admin/update_status/<int:contact_id>', methods=['POST'])
def update_status(contact_id):
    if not check_admin():
        return jsonify({'success': False}), 401
    try:
        data = request.json
        new_status = data.get('status')
        for contact in contacts_data:
            if contact['id'] == contact_id:
                contact['status'] = new_status
                return jsonify({'success': True})
        return jsonify({'success': False}), 404
    except:
        return jsonify({'success': False}), 500

# Static files


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/api/content')
def api_content():
    """API endpoint for real-time content updates"""
    return jsonify(load_content())


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(host="0.0.0.0", port=port)

    # Initialize content file
    if not os.path.exists(CONTENT_FILE):
        save_content(DEFAULT_CONTENT.copy())

    print("=" * 60)
    print("🌟 WONDERLAND EDUCATIONAL CONSULTANCY CMS 🌟")
    print("=" * 60)
    print("🌐 Website:        http://localhost:5000")
    print("🔐 Admin Login:    http://localhost:5000/admin/login")
    print("   👤 Username:    admin")
    print("   🔑 Password:    admin123")
    print("-" * 60)
    print("📝 Content Editor: http://localhost:5000/admin/content")
    print("📊 Dashboard:      http://localhost:5000/admin/dashboard")
    print("📋 Contacts:       http://localhost:5000/admin/contacts")
    print("=" * 60)

    app.run(debug=True, port=5000)
