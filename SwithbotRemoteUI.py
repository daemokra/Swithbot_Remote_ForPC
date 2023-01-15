from dotenv import load_dotenv
import os
from switchbotpy import SwitchBotPy

load_dotenv()
TOKEN  = os.getenv('TOKEN')
SECRET = os.getenv('SECRET')

switchbot = SwitchBotPy(token=TOKEN, secret=SECRET, nonce='' ,version='v1.1')

aircon = switchbot.get_airconditioners()
aircon[0].temperature = '19'
aircon[0].mode        = 'heat'
aircon[0].speed       = 'low'
result = aircon[0].turn_on()
print(aircon[0].get_status())

