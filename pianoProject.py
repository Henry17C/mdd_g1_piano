import cv2
import mediapipe as mp
import pygame

# Inicializar pygame para los sonidos
pygame.init()

# Cargar sonidos de las notas (asegúrate de tener estos archivos en la misma carpeta)
notas = {
    "Do": pygame.mixer.Sound("do.mp3"),
    "Re": pygame.mixer.Sound("re.mp3"),
    "Mi": pygame.mixer.Sound("mi.mp3"),
    "Fa": pygame.mixer.Sound("fa.mp3"),
    "Sol": pygame.mixer.Sound("sol.mp3"),
    "La": pygame.mixer.Sound("la.mp3"),
    "Si": pygame.mixer.Sound("si.mp3"),
    "Do2": pygame.mixer.Sound("do2.mp3"),
}

# Cargar la imagen del piano
piano_img = cv2.imread("piano.png")

# Ajustar el tamaño de la imagen del piano
piano_width, piano_height = 800, 200
piano_img = cv2.resize(piano_img, (piano_width, piano_height))

# Inicializar Mediapipe para detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Iniciar captura de video
cap = cv2.VideoCapture(0)

# Definir posiciones de teclas en la imagen (ajusta según tu imagen)
teclas = {
    "Do":  (0, 200, 100, 400),
    "Re":  (100, 200, 200, 400),
    "Mi":  (200, 200, 300, 400),
    "Fa":  (300, 200, 400, 400),
    "Sol": (400, 200, 500, 400),
    "La":  (500, 200, 600, 400),
    "Si":  (600, 200, 700, 400),
    "Do2": (700, 200, 800, 400),
}



tecla_anterior = None  # Para evitar que suene muchas veces una misma tecla

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Espejar la imagen para que sea más intuitivo
    frame = cv2.flip(frame, 1)

    # Obtener tamaño del video
    frame_height, frame_width, _ = frame.shape
    frame = cv2.resize(frame, (piano_width, 480))

    # Convertir la imagen a RGB para Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Dibujar la imagen del piano en la parte inferior
    frame[280:280+piano_height, 0:piano_width] = piano_img

    # Si se detectan manos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Obtener coordenadas del dedo índice (índice 8 en Mediapipe)
            x, y = int(hand_landmarks.landmark[8].x * piano_width), int(hand_landmarks.landmark[8].y * 480)

            # Dibujar un círculo en el dedo índice
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Verificar si el dedo toca alguna tecla
            tecla_presionada = None
            for nota, (x1, y1, x2, y2) in teclas.items():
                if x1 < x < x2 and y1 < y < y2:
                    tecla_presionada = nota
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Resaltar tecla

            # Si se detecta una nueva tecla presionada, reproducir sonido
            if tecla_presionada and tecla_presionada != tecla_anterior:
                notas[tecla_presionada].play()
                tecla_anterior = tecla_presionada
            elif tecla_presionada is None:
                tecla_anterior = None  # Resetear si no hay teclas presionadas

            # Dibujar los puntos de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostrar la ventana
    cv2.imshow("Piano Virtual", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
