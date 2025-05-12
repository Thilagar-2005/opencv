import cv2
import geocoder
import pywhatkit
import datetime


img1 = cv2.imread(r'C:\Users\THILAGAR.S\Pictures\Road\goodOne.webp')   
img2 = cv2.imread(r'C:\Users\THILAGAR.S\Pictures\Road\damageOne.webp') 


img1 = cv2.resize(img1, (500, 500))
img2 = cv2.resize(img2, (500, 500))


gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


diff = cv2.absdiff(gray1, gray2)
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)


contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
non_zero_count = cv2.countNonZero(thresh)


for contour in contours:
    if cv2.contourArea(contour) > 500:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 3)


def get_location():
    g = geocoder.ip('me')
    latlng = g.latlng
    location = f"{g.city}, {g.state}, {g.country}"
    maps_link = f"https://www.google.com/maps?q={latlng[0]},{latlng[1]}"
    return location, maps_link


if non_zero_count > 5000:
    print("🚧 Road damage detected!")

    
    cv2.imshow("Detected Damage", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    saved_path = r"C:\Users\THILAGAR.S\Pictures\Road\DetectedDamageOutput.jpg"
    cv2.imwrite(saved_path, img2)

    
    location, maps_link = get_location()
    print("📍 Location:", location)
    print("🌍 Google Maps:", maps_link)

    
    phone_number = "+917695871421"  # Replace with real number
    caption = f"""🚧 Damage detected!
📍 {location}
🌍 {maps_link}"""

    now = datetime.datetime.now()
    pywhatkit.sendwhats_image(
        receiver=phone_number,
        img_path=saved_path,
        caption=caption,
        wait_time=15
    )

else:
    print("✅ Road is in good condition.")
    cv2.imshow("Detected Damage", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
