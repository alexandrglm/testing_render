############################################################################
# CONTACT PAGE -> API, VALIDATIONS, SMTP
#############
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from flask import jsonify, request

load_dotenv()

class ContactMail:
    def __init__(self):
        
        self.smtp_config = {
            'server': os.getenv('SMTP_SERVER'),
            'port': int(os.getenv('SMTP_PORT')),
            'user': os.getenv('SMTP_USER'),
            'password': os.getenv('SMTP_PASSWORD'),
            'account': os.getenv('SMTP_ACCOUNT')
        }

    def smtp_config_validation(self):


        if not self.smtp_config['password']:

            raise ValueError('DEBUG (SMTP) -> SMTP Config not found!')

    def send_contact_form(self, mail_data):

        self.smtp_config_validation()

        msg = MIMEText(
            f'''New message received from Contact form!

            -----------------------------------------
            From:    {mail_data['name'].strip()} - {mail_data['email'].strip()}
            Date: {datetime.now().strftime('%Y, %m. %d - %H:%M:%S')}
            -----------------------------------------

            - Message -
            {mail_data['message'].strip()}

            -----------------------------------------
            ''')

        msg['Subject'] = f'JustLearning CONTACT from -> {mail_data["name"]}'
        msg['From'] = self.smtp_config['user']
        msg['To'] = self.smtp_config['account']

        with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
            server.starttls()
            server.login(self.smtp_config['user'], self.smtp_config['password'])
            server.send_message(msg)

def start_server_email(app):
    @app.route('/sendmail/', methods=['POST'])
    def contact_email():
        try:
            if not request.is_json:
                print('DEBUG Contact -> Error Sending -> JSON error')
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            mail_data = request.get_json()
            all_required_fields = ['name', 'email', 'message']
            
            if not all(field in mail_data for field in all_required_fields):
                return jsonify({'error': 'Missing required fields'}), 400


            mail_service = ContactMail()
            mail_service.send_contact_form(mail_data)
            
            return jsonify({'message': 'Message sent!'}), 200

        except ValueError as e:

            print(f'DEBUG (Contact) -> Config fail! (env?): {str(e)}')
            return jsonify({'error': str(e)}), 500
        
        except Exception as e:

            print(f'DEBUG (Contact/SMTP) -> Unexpected error: {str(e)}')
            return jsonify({'error': 'Internal server error (is server on?)'}), 500