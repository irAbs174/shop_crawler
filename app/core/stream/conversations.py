# CLIENT CONVERSATIONS
from .dbConf import *
from target.models import TargetModel
from products.models import Product

def socket_conversation(message):
    data = message.decode()
    print(f"DATA =>>> {data}")
    if data.split(',')[1] == 'READY':
        url = TargetModel.objects.all().filter(targetName="buykif")[0].targetUrl
        return b"200,TARGET,url"
    else:
        return b'end'