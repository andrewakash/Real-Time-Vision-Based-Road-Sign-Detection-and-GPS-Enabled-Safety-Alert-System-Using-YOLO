from pyngrok import ngrok
import time

public_url = ngrok.connect(5000)

print("NGROK URL:")
print(public_url)

print("Tunnel Running...")

while True:
    time.sleep(1)