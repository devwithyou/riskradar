#!/usr/bin/env python
"""
Demo Data Creator for WebGuard Security Scanner
Creates sample scan data for demonstration purposes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webguard.settings')
django.setup()

from django.contrib.auth.models import User
from analyzer.models import ScanResult, Issue

def create_demo_data():
    print("🛡️  Creating demo data for WebGuard...")
    print("=" * 50)
    
    # Create demo user if doesn't exist
    demo_user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@webguard.com',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        demo_user.set_password('demo123')
        demo_user.save()
        print("✅ Created demo user: username='demo', password='demo123'")
    else:
        print("ℹ️  Demo user already exists")
    
    # Sample scan data
    demo_scans = [
        {
            'url': 'https://google.com',
            'final_url': 'https://www.google.com/',
            'status_code': 200,
            'score': 85,
            'headers': {
                'Content-Security-Policy': "default-src 'self'",
                'Strict-Transport-Security': 'max-age=31536000',
                'X-Frame-Options': 'SAMEORIGIN',
                'X-Content-Type-Options': 'nosniff'
            },
            'issues': [
                {
                    'severity': 'low',
                    'category': 'Permissions-Policy',
                    'message': 'Missing Permissions-Policy header',
                    'recommendation': 'Add Permissions-Policy header to control browser features and APIs.'
                },
                {
                    'severity': 'medium',
                    'category': 'Referrer-Policy',
                    'message': 'Missing Referrer-Policy header',
                    'recommendation': 'Add Referrer-Policy header to control referrer information.'
                }
            ]
        },
        {
            'url': 'http://example.com',
            'final_url': 'http://example.com/',
            'status_code': 200,
            'score': 22,
            'headers': {
                'Content-Type': 'text/html; charset=UTF-8',
                'Server': 'Apache'
            },
            'issues': [
                {
                    'severity': 'high',
                    'category': 'HTTPS',
                    'message': 'Site is not using HTTPS encryption',
                    'recommendation': 'Enable HTTPS to encrypt data in transit.'
                },
                {
                    'severity': 'high',
                    'category': 'Content-Security-Policy',
                    'message': 'Missing Content-Security-Policy header',
                    'recommendation': 'Add CSP header to prevent XSS attacks.'
                },
                {
                    'severity': 'high',
                    'category': 'HSTS',
                    'message': 'Missing Strict-Transport-Security header',
                    'recommendation': 'Add HSTS header to force HTTPS connections.'
                },
                {
                    'severity': 'medium',
                    'category': 'X-Frame-Options',
                    'message': 'Missing X-Frame-Options header',
                    'recommendation': 'Add X-Frame-Options to prevent clickjacking.'
                }
            ]
        },
        {
            'url': 'https://github.com',
            'final_url': 'https://github.com/',
            'status_code': 200,
            'score': 92,
            'headers': {
                'Content-Security-Policy': "default-src 'none'",
                'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
                'X-Frame-Options': 'deny',
                'X-Content-Type-Options': 'nosniff',
                'Referrer-Policy': 'origin-when-cross-origin'
            },
            'issues': [
                {
                    'severity': 'low',
                    'category': 'Permissions-Policy',
                    'message': 'Missing Permissions-Policy header',
                    'recommendation': 'Add Permissions-Policy header for better browser feature control.'
                }
            ]
        }
    ]
    
    # Create scans
    for scan_data in demo_scans:
        # Check if scan already exists
        existing = ScanResult.objects.filter(url=scan_data['url']).first()
        if existing:
            print(f"ℹ️  Scan for {scan_data['url']} already exists, skipping...")
            continue
        
        # Create scan result
        scan = ScanResult.objects.create(
            url=scan_data['url'],
            final_url=scan_data['final_url'],
            status_code=scan_data['status_code'],
            score=scan_data['score'],
            raw_headers=scan_data['headers'],
            owner=demo_user
        )
        
        # Create issues
        for issue_data in scan_data['issues']:
            Issue.objects.create(
                scan_result=scan,
                severity=issue_data['severity'],
                category=issue_data['category'],
                message=issue_data['message'],
                recommendation=issue_data['recommendation']
            )
        
        print(f"✅ Created scan for {scan_data['url']} (Score: {scan_data['score']})")
    
    print("\n" + "=" * 50)
    print("✨ Demo data creation complete!")
    print("\n📝 Demo Account:")
    print("   Username: demo")
    print("   Password: demo123")
    print("\n🌐 You can now:")
    print("   1. Login with demo/demo123")
    print("   2. View scan history")
    print("   3. See sample results")
    print("   4. Run new scans")

if __name__ == '__main__':
    create_demo_data()


