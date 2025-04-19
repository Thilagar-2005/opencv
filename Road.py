import cv2
import geocoder
import smtplib
from email.mime.text import MIMEText

# ------------------------------
# Step 1: Load road images
# ------------------------------
img1 = cv2.imread(r'C:\Users\THILAGAR.S\Pictures\Road\goodOne.webp')   # Good road image
img2 = cv2.imread(r'C:\Users\THILAGAR.S\Pictures\Road\damageOne.webp') # Damaged road image

# Resize both to same size
img1 = cv2.resize(img1, (500, 500))
img2 = cv2.resize(img2, (500, 500))

# Convert to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Compute absolute difference
diff = cv2.absdiff(gray1, gray2)

# Threshold to highlight changes
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

# Count the number of changed pixels
non_zero_count = cv2.countNonZero(thresh)

# Show the differences
cv2.imshow("Difference", diff)
cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------------------------------
# Step 2: Get user location (city, state, country, lat-lng)
# ------------------------------
def get_location():
    g = geocoder.ip('me')
    latlng = g.latlng
    location = f"{g.city}, {g.state}, {g.country}"
    maps_link = f"https://www.google.com/maps?q={latlng[0]},{latlng[1]}"
    return location, maps_link

# ------------------------------
# Step 3: Send email with location
# ------------------------------
def send_email(location, maps_link):
    sender_email = "thilagar.ts2005@gmail.com"       # Change this
    receiver_email = "sabarinarayanan10@gmail.com" # Change this
    password = "Thila@2005"              # Use Gmail App Password

    subject = "🚧 Road Damage Detected!"
    body = f"""Road damage has been detected at the following location:

📍 Location: {location}
📌 Map: {maps_link}

Please take necessary action.

- Automatic Road Issue Detection System
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📧 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ------------------------------
# Step 4: Decision & Notification
# ------------------------------
if non_zero_count > 5000:
    print("🚧 Road damage detected!")
    location, maps_link = get_location()
    print("📍 Location:", location)
    print("📌 Google Maps:", maps_link)
    send_email(location, maps_link)
else:
    print("✅ Road is in good condition.")
