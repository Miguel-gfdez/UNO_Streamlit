from supabase import create_client
import os


def get_client():
    try:
        url = os.getenv("SUPABASE_URL")
        # url = SUPABASE_URL if url is None else url
        key = os.getenv("SUPABASE_KEY")
        # key = SUPABASE_KEY if key is None else key
    except Exception as e:
        url = " "
        key = " "

    supabase = create_client(url, key)
    return supabase



