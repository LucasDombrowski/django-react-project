from django.shortcuts import redirect
from django.urls import reverse

class AuthenticatedUserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the paths for login and registration pages
            login_url = reverse('login')
            register_url = reverse('register')

            if request.path == login_url or request.path == register_url:
                # Redirect to the home page or a dashboard
                # For now, we'll redirect to the root path '/'
                return redirect('/') 
        
        response = self.get_response(request)
        return response 