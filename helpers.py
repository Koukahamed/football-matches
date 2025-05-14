import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests


# Fonction pour récupérer les matchs d'aujourd'hui
def fetch_todays_matches(api_key):
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": api_key}

    # Renommage des codes de compétitions
    competition_names = {
        "PD": "Liga Espagnole",
        "FL1": "Ligue 1 Française",
        "SA": "Serie A Italienne",
        "PL": "Premier League Anglaise",
        "CL": "Ligue des Champions",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        matches = data.get("matches", [])

        # Filtrer les matchs selon les compétitions majeures
        filtered_matches = []
        for match in matches:
            code = match["competition"]["code"]
            if code in competition_names:
                filtered_matches.append(
                    {
                        "Competition": competition_names[code],
                        "HomeTeam": match["homeTeam"]["name"],
                        "AwayTeam": match["awayTeam"]["name"],
                        "Date": match["utcDate"],
                    }
                )

        return filtered_matches

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des matchs : {e}")
        return []


# Fonction pour formater le corps HTML des matchs
def format_matches_html(matches):
    if not matches:
        return "<h2>Aucun match trouvé pour aujourd'hui.</h2>"

    body = "<h2>Matchs d'aujourd'hui</h2>"
    for match in matches:
        # Convertir la date au format JJ/MM/AAAA
        match_date = datetime.strptime(match["Date"], "%Y-%m-%dT%H:%M:%SZ").strftime(
            "%d/%m/%Y"
        )

        body += f"""
        <p><strong>Compétition :</strong> {match['Competition']}</p>
        <p><strong>Match :</strong> {match['HomeTeam']} vs {match['AwayTeam']}</p>
        <p><strong>Date :</strong> {match_date}</p>
        <hr>
        """
    return body


# Fonction pour envoyer un e-mail
def send_email(
    subject,
    body,
    mail_user,
    mail_pass,
    to_email,
    is_html=True,
    smtp_server="smtp.gmail.com",
    smtp_port=465,
):
    try:
        msg = MIMEMultipart()
        msg["From"] = mail_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if is_html else "plain"))

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(mail_user, mail_pass)
            server.sendmail(mail_user, to_email, msg.as_string())

        print("✅ E-mail envoyé avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")
