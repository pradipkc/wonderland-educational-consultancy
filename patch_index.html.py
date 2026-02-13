# patch_index.html.py
import re

def update_index_html():
    # Read the current index.html
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace hero title
    content = re.sub(
        r'<h1 class="hero-title">[^<]+</h1>',
        '<h1 class="hero-title">{{ content.hero.title if content and content.hero and content.hero.title else "Unlocking Your Academic Future" }}</h1>',
        content
    )
    
    # Replace hero subtitle
    content = re.sub(
        r'<p class="hero-subtitle">[^<]+</p>',
        '<p class="hero-subtitle">{{ content.hero.subtitle if content and content.hero and content.hero.subtitle else "Expert guidance for international students to achieve their educational dreams. With over 15 years of experience, we\'ve helped 5000+ students secure admissions in top universities worldwide." }}</p>',
        content
    )
    
    # Replace statistics
    stat_pattern = r'<div class="hero-stats">[\s\S]*?</div>'
    new_stats = '''<div class="hero-stats">
    <div class="stat-item">
        <span class="stat-number">{{ content.hero.stat1_number if content and content.hero and content.hero.stat1_number else "98%" }}</span>
        <span class="stat-text">{{ content.hero.stat1_text if content and content.hero and content.hero.stat1_text else "Success Rate" }}</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">{{ content.hero.stat2_number if content and content.hero and content.hero.stat2_number else "5000+" }}</span>
        <span class="stat-text">{{ content.hero.stat2_text if content and content.hero and content.hero.stat2_text else "Students Helped" }}</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">{{ content.hero.stat3_number if content and content.hero and content.hero.stat3_number else "50+" }}</span>
        <span class="stat-text">{{ content.hero.stat3_text if content and content.hero and content.hero.stat3_text else "Countries" }}</span>
    </div>
</div>'''
    
    content = re.sub(stat_pattern, new_stats, content, flags=re.DOTALL)
    
    # Replace services title
    content = re.sub(
        r'<h2 class="section-title">Our Premium Services</h2>',
        '<h2 class="section-title">{{ content.services.title if content and content.services and content.services.title else "Our Premium Services" }}</h2>',
        content
    )
    
    # Replace services subtitle
    content = re.sub(
        r'<p class="section-subtitle">Comprehensive support for your educational journey</p>',
        '<p class="section-subtitle">{{ content.services.subtitle if content and content.services and content.services.subtitle else "Comprehensive support for your educational journey" }}</p>',
        content
    )
    
    # Save the updated file
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Updated index.html with dynamic content placeholders")
    print("✓ Hero section, statistics, and services titles are now dynamic")

if __name__ == '__main__':
    update_index_html()