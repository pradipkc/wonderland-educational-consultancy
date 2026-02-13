# test_dynamic_content.py
from app import app, db, WebsiteContent

with app.app_context():
    # Test if database has content
    content_items = db.session.execute(db.select(WebsiteContent)).scalars().all()
    print(f"Total content items in database: {len(content_items)}")
    
    if content_items:
        print("\nSample content:")
        for item in content_items[:5]:  # Show first 5 items
            print(f"{item.section}.{item.content_key}: {item.content_value[:50]}...")
    else:
        print("No content found in database!")