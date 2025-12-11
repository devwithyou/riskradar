"""
Security Scanner Engine
Analyzes URLs for security issues and generates a score
"""
import requests
from urllib.parse import urlparse


class SecurityScanner:
    """Main security scanner class"""
    
    def __init__(self):
        self.score = 100
        self.issues = []
    
    def scan_url(self, url):
        """
        Scan a URL and return security analysis
        Returns: dict with score, issues, headers, status_code, final_url
        """
        try:
            # Fetch URL
            response = requests.get(
                url,
                allow_redirects=True,
                timeout=10,
                headers={'User-Agent': 'WebGuard Security Scanner/1.0'}
            )
            
            final_url = response.url
            status_code = response.status_code
            headers = dict(response.headers)
            cookies = response.cookies
            
            # Reset for new scan
            self.score = 100
            self.issues = []
            
            # Run security checks
            self._check_https(final_url)
            self._check_security_headers(headers)
            self._check_cookies(cookies)
            
            return {
                'score': max(self.score, 0),  # Don't go below 0
                'issues': self.issues,
                'headers': headers,
                'status_code': status_code,
                'final_url': final_url,
            }
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def _add_issue(self, severity, category, message, recommendation, points):
        """Add an issue and deduct points"""
        self.issues.append({
            'severity': severity,
            'category': category,
            'message': message,
            'recommendation': recommendation,
        })
        self.score -= points
    
    def _check_https(self, url):
        """Check if URL uses HTTPS"""
        parsed = urlparse(url)
        if parsed.scheme != 'https':
            self._add_issue(
                severity='high',
                category='HTTPS',
                message='Site is not using HTTPS encryption',
                recommendation='Enable HTTPS to encrypt data in transit. Obtain an SSL/TLS certificate from a trusted Certificate Authority.',
                points=20
            )
    
    def _check_security_headers(self, headers):
        """Check for security headers"""
        
        # Content-Security-Policy (CSP)
        if 'Content-Security-Policy' not in headers:
            self._add_issue(
                severity='high',
                category='Content-Security-Policy',
                message='Missing Content-Security-Policy header',
                recommendation='Add CSP header to prevent XSS attacks and control resource loading.',
                points=15
            )
        
        # Strict-Transport-Security (HSTS)
        if 'Strict-Transport-Security' not in headers:
            self._add_issue(
                severity='high',
                category='HSTS',
                message='Missing Strict-Transport-Security header',
                recommendation='Add HSTS header to force HTTPS connections and prevent protocol downgrade attacks.',
                points=15
            )
        
        # X-Frame-Options
        if 'X-Frame-Options' not in headers:
            self._add_issue(
                severity='medium',
                category='X-Frame-Options',
                message='Missing X-Frame-Options header',
                recommendation='Add X-Frame-Options header to prevent clickjacking attacks.',
                points=10
            )
        
        # X-Content-Type-Options
        if 'X-Content-Type-Options' not in headers:
            self._add_issue(
                severity='medium',
                category='X-Content-Type-Options',
                message='Missing X-Content-Type-Options header',
                recommendation='Add X-Content-Type-Options: nosniff to prevent MIME type sniffing.',
                points=8
            )
        
        # Referrer-Policy
        if 'Referrer-Policy' not in headers:
            self._add_issue(
                severity='medium',
                category='Referrer-Policy',
                message='Missing Referrer-Policy header',
                recommendation='Add Referrer-Policy header to control referrer information sent to other sites.',
                points=7
            )
        
        # Permissions-Policy (formerly Feature-Policy)
        if 'Permissions-Policy' not in headers and 'Feature-Policy' not in headers:
            self._add_issue(
                severity='low',
                category='Permissions-Policy',
                message='Missing Permissions-Policy header',
                recommendation='Add Permissions-Policy header to control browser features and APIs.',
                points=5
            )
        
        # X-XSS-Protection (legacy but still useful)
        if 'X-XSS-Protection' not in headers:
            self._add_issue(
                severity='low',
                category='X-XSS-Protection',
                message='Missing X-XSS-Protection header',
                recommendation='Add X-XSS-Protection header for legacy browser XSS protection.',
                points=3
            )
    
    def _check_cookies(self, cookies):
        """Check cookie security attributes"""
        for cookie in cookies:
            cookie_name = cookie.name
            
            # Check Secure flag
            if not cookie.secure:
                self._add_issue(
                    severity='high',
                    category='Cookie Security',
                    message=f'Cookie "{cookie_name}" missing Secure flag',
                    recommendation='Set Secure flag on cookies to ensure they are only sent over HTTPS.',
                    points=10
                )
            
            # Check HttpOnly flag
            if not cookie.has_nonstandard_attr('HttpOnly'):
                self._add_issue(
                    severity='medium',
                    category='Cookie Security',
                    message=f'Cookie "{cookie_name}" missing HttpOnly flag',
                    recommendation='Set HttpOnly flag on cookies to prevent JavaScript access and XSS attacks.',
                    points=8
                )
            
            # Check SameSite attribute
            samesite = cookie.get_nonstandard_attr('SameSite')
            if not samesite:
                self._add_issue(
                    severity='low',
                    category='Cookie Security',
                    message=f'Cookie "{cookie_name}" missing SameSite attribute',
                    recommendation='Set SameSite attribute on cookies to prevent CSRF attacks (use Strict or Lax).',
                    points=5
                )


