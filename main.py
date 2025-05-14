import os

from dotenv import load_dotenv

from helpers import fetch_todays_matches, format_matches_html, send_email

# Charger les variables d'environnement
load_dotenv(dotenv_path=".env")

api_key = os.getenv("FOOTBALL_API_KEY")
mail_user = os.getenv("MAIL_USER")
mail_pass = os.getenv("MAIL_PASS")
to_email = mail_user

matches = fetch_todays_matches(api_key)
html = format_matches_html(matches)

send_email(
    subject="⚽ Matchs du jour",
    body=html,
    mail_user=mail_user,
    mail_pass=mail_pass,
    to_email=to_email,
    is_html=True,
)
