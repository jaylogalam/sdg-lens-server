from supabase import Client
from models import ProfileModel

class ProfileServices:
    @staticmethod
    def initialize_profile(user: ProfileModel, db: Client):
        ...