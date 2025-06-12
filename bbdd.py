from supabase import create_client
import os


def get_client():
    try:
        url = "https://rzzebfnvgicvovhkqcyi.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6emViZm52Z2ljdm92aGtxY3lpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2MzI0NzUsImV4cCI6MjA2NTIwODQ3NX0.LhgN8mKzsd2-wvoZkzkIvRhkvfjg6g-QjFMZgzBxwfM"
        # url = os.getenv("SUPABASE_URL")
        # # url = SUPABASE_URL if url is None else url
        # key = os.getenv("SUPABASE_KEY")
        # key = SUPABASE_KEY if key is None else key
    except Exception as e:
        url = " "
        key = " "

    supabase = create_client(url, key)
    return supabase



