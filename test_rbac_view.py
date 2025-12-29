from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from veteran_app.models import Role, Permission, UserRole

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def test_rbac(request):
    """Simple test view for RBAC"""
    users = User.objects.all()[:10]  # Get first 10 users
    roles = Role.objects.filter(is_active=True)
    
    context = {
        'users': users,
        'roles': roles,
        'user_count': User.objects.count(),
        'role_count': roles.count()
    }
    
    return render(request, 'veteran_app/test_rbac.html', context)