# minimal_test.py
print("Testing Flask setup...")

try:
    from app import app, db
    print("✓ Import successful")
    
    with app.app_context():
        db.create_all()
        print("✓ Database created")
        
        # Check if we can query
        from app import WebsiteContent
        count = db.session.query(WebsiteContent).count()
        print(f"✓ WebsiteContent records: {count}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()