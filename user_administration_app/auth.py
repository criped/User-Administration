
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        user.is_staff = 1
        user.save(update_fields=["is_staff"])
