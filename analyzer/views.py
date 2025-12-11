from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScanResult, Issue
from .scanner import SecurityScanner


def home(request):
    """Landing page"""
    return render(request, 'analyzer/home.html')


def scan(request):
    """URL scan page"""
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        if not url:
            messages.error(request, 'Please enter a valid URL.')
            return render(request, 'analyzer/scan.html')
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            scanner = SecurityScanner()
            result_data = scanner.scan_url(url)
            
            # Save to database
            scan_result = ScanResult.objects.create(
                url=url,
                final_url=result_data['final_url'],
                status_code=result_data['status_code'],
                score=result_data['score'],
                raw_headers=result_data['headers'],
                owner=request.user if request.user.is_authenticated else None
            )
            
            # Save issues
            for issue in result_data['issues']:
                Issue.objects.create(
                    scan_result=scan_result,
                    severity=issue['severity'],
                    category=issue['category'],
                    message=issue['message'],
                    recommendation=issue['recommendation']
                )
            
            return redirect('result', scan_id=scan_result.id)
        
        except Exception as e:
            messages.error(request, f'Error scanning URL: {str(e)}')
            return render(request, 'analyzer/scan.html')
    
    return render(request, 'analyzer/scan.html')


def result(request, scan_id):
    """Scan results page"""
    scan_result = get_object_or_404(ScanResult, id=scan_id)
    issues_by_severity = {
        'high': scan_result.issues.filter(severity='high'),
        'medium': scan_result.issues.filter(severity='medium'),
        'low': scan_result.issues.filter(severity='low'),
    }
    
    context = {
        'scan': scan_result,
        'issues_by_severity': issues_by_severity,
    }
    return render(request, 'analyzer/result.html', context)


def history(request):
    """Scan history page (requires login)"""
    if not request.user.is_authenticated:
        return render(request, 'analyzer/history.html', {'scans': None})
    
    scans = ScanResult.objects.all()[:50]  # Last 50 scans
    return render(request, 'analyzer/history.html', {'scans': scans})


@login_required
def my_scans(request):
    """User's own scans"""
    scans = ScanResult.objects.filter(owner=request.user)
    return render(request, 'analyzer/my_scans.html', {'scans': scans})


def login_view(request):
    """Login page"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'analyzer/login.html', {'form': form})


def logout_view(request):
    """Logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_view(request):
    """Registration page"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'analyzer/register.html', {'form': form})

