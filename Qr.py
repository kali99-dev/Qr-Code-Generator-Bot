import telebot
import qrcode
from io import BytesIO
import re

# Replace with your bot token from @BotFather
BOT_TOKEN = '7895657453:AAE0sAylCvQJD4WOfZ35Ucz975odzB3voHc'

bot = telebot.TeleBot(BOT_TOKEN)

def generate_qr(data):
    """Generate QR code and return as bytes"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to bytes
    bio = BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = """
🤖 *QR Code Generator Bot*

Send me any of the following and I'll generate a QR code:

📱 *Phone Number:*
`+1234567890` or just `1234567890`

🌐 *URL:*
`https://example.com`

📝 *Text:*
Any text message

👤 *Contact (vCard format):*
```
BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD
```

Just send the content and I'll create your QR code! 🎯
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text.strip()
        
        # Detect type and format data
        if text.startswith('BEGIN:VCARD'):
            qr_data = text
            data_type = "Contact vCard"
        elif re.match(r'^[\+]?[\d\s\-\(\)]+$', text):
            # Phone number
            phone = re.sub(r'[\s\-\(\)]', '', text)
            if not phone.startswith('+'):
                phone = '+' + phone
            qr_data = f"tel:{phone}"
            data_type = "Phone Number"
        elif text.startswith(('http://', 'https://', 'www.')):
            # URL
            qr_data = text
            data_type = "URL"
        else:
            # Plain text
            qr_data = text
            data_type = "Text"
        
        # Generate QR code
        qr_image = generate_qr(qr_data)
        
        # Send QR code
        bot.send_photo(
            message.chat.id,
            qr_image,
            caption=f"✅ QR Code generated for {data_type}\n\n`{text[:100]}{'...' if len(text) > 100 else ''}`",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error generating QR code: {str(e)}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()