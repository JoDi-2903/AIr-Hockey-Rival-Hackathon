import cv2

# Kamera-Index (meist 0 für die erste angeschlossene Kamera)
camera_index = 1

# Öffne die Kamera
cap = cv2.VideoCapture(camera_index)  # Optional: CAP_DSHOW für Windows Performance

# Setze die Auflösung auf Full HD
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Überprüfe, ob die Kamera geöffnet wurde
if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

print("Drücke 'q' zum Beenden.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kein Frame erhalten.")
        break

    # Optional: Frame anzeigen
    cv2.imshow('USB Kamera - Full HD', frame)

    # Beenden mit Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera und Fenster freigeben
cap.release()
cv2.destroyAllWindows()
