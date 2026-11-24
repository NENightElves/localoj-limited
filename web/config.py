import uuid


SECRET = str(uuid.uuid4())[0:8]
HOST = '0.0.0.0'
PORT = 6666
QUESTIONS = {
    'q1': (3, ''),
    'q2': (18, 'copycat')
}

print(SECRET)
