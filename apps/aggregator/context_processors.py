def context(request):
    social_auth = None
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        social_auth = user.social_auth.filter(provider='unti').first()
    return {
        'USER_SOCIAL_AUTH': social_auth,
    }
