from fly_project import constants


def app_constants(request):
    """Attaches all our constants to every template."""
    return {
        'constants': constants,
    }
