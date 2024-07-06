# SERVER CONVERSATIONS
#.startswith('https://') or address.startswith('http://'):
def socket_conversation(message):
    if message.decode() == '174':
        return b"200,READY"
    elif message.decode().split(',')[1] == 'TARGET':
        return b'SUCCESS'
    else:
        return b'end'