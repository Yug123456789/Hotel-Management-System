def user_verification_status(request):
    is_verified = False
    if request.user.is_authenticated:
        try:
            is_verified = request.user.profile.verified
        except:
            pass
    return {'is_verified': is_verified}