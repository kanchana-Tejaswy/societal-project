import qrcode

url = "http://192.168.31.249:5000"

qr = qrcode.make(url)

qr.save("collection_qr.png")

print("QR Code Generated Successfully!")