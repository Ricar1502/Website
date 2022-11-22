from api.models import Profile


def get_user(request):

    if request.user.is_authenticated:
        user = request.user
        this_profile = Profile.objects.get(user=user)
        return {'this_profile': this_profile}  # of course some filter here
    return {}
