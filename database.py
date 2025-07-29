from supabase import create_client
import os


url=os.getenv("SUPABASE_URL","https://pqlvxcupcthftoquxlut.supabase.co")
key=os.getenv("SUPABASE_KEY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBxbHZ4Y3VwY3RoZnRvcXV4bHV0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMwODM3OTUsImV4cCI6MjA2ODY1OTc5NX0.4swIjzF_VMm5s4BCAiEh-dBL8E8jYmWiaZoSdobisVU")

supabase=create_client(url,key)