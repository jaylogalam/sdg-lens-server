from database import SupabaseClient
_db = SupabaseClient.get_client().from_("profiles")

class ProfileServices:
    ...
    # @classmethod
    # def init_profile()