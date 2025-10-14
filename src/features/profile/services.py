from .model import ProfileModel

def initialize_profile(profile: ProfileModel):
    # Step 2: Create profile record
    profile = {
        "id": profile.id,
        "username": profile.username,
    }

    profile_response = db.table("profiles").insert(profile).execute()
    if profile_response.error:
        return "profile creation error"

    return "Success"