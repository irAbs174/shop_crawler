# CLIENT CONVERSATIONS

def socket_conversation(message):
    data = message.decode()
    print(f"DATA =>>> {data}")
    if data.split(',')[1] == 'READY':
        return b"200,TARGET,https://target.com"
    else:
        return b'end'