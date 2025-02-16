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
    "Do#": pygame.mixer.Sound("re.mp3"),
    "Re#": pygame.mixer.Sound("re.mp3"),
    "Fa#": pygame.mixer.Sound("re.mp3"),
    "Sol#": pygame.mixer.Sound("re.mp3"),
    "La#": pygame.mixer.Sound("re.mp3"),
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
teclas_blancas = {
    "Do":  (0, 250, 100, 470),
    "Re":  (100, 250, 200, 470),
    "Mi":  (200, 250, 300, 470),
    "Fa":  (300, 250, 400, 470),
    "Sol": (400, 250, 500, 470),
    "La":  (500, 250, 600, 470),
    "Si":  (600, 250, 700, 470),
    "Do2": (700, 250, 800, 470),
}

teclas_negras = {
    "Do#": (75, 250, 125, 350),
    "Re#": (175, 250, 225, 350),
    "Fa#": (375, 250, 425, 350),
    "Sol#": (475, 250, 525, 350),
    "La#": (575, 250, 625, 350),
}

tecla_anterior = None  # Para evitar que suene muchas veces una misma tecla
tecla_presionada = None  # Inicializar tecla_presionada

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

    # Dibujar las teclas blancas del piano con sombra y bordes curvados
    for nota, (x1, y1, x2, y2) in teclas_blancas.items():
        shadow_color = (192, 192, 192)  # Gris claro para la sombra
        border_color = (169, 169, 169)  # Plomo para el borde inferior
        color = (255, 255, 255)  # Blanco
        if tecla_presionada == nota:
            color = (169, 169, 169)  # Plomo
            shadow_color = (105, 105, 105)  # Gris oscuro para la sombra cuando se presiona
        # Dibujar sombra
        cv2.rectangle(frame, (x1 + 5, y1 + 5), (x2 + 5, y2 + 5), shadow_color, -1)
        # Dibujar tecla con bordes curvados
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)  # Relleno
        cv2.rectangle(frame, (x1, y2 - 10), (x2, y2), border_color, -1)  # Borde inferior curvado
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Borde negro

    # Dibujar las teclas negras del piano con sombra ajustada
    for nota, (x1, y1, x2, y2) in teclas_negras.items():
        shadow_color = (64, 64, 64)  # Gris oscuro para la sombra
        color = (0, 0, 0)  # Negro
        if tecla_presionada == nota:
            color = (105, 105, 105)  # Gris oscuro
            shadow_color = (32, 32, 32)  # Más oscuro para la sombra cuando se presiona
        # Dibujar sombra desde el inicio del piano
        cv2.rectangle(frame, (x1 + 5, 250), (x2 + 5, y2 + 5), shadow_color, -1)
        # Dibujar tecla
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)  # Relleno
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Borde negro

    # Si se detectan manos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Obtener coordenadas del dedo índice (índice 8 en Mediapipe)
            x, y = int(hand_landmarks.landmark[8].x * piano_width), int(hand_landmarks.landmark[8].y * 480)

            # Dibujar un círculo en el dedo índice
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Verificar si el dedo toca alguna tecla
            tecla_presionada = None
            for nota, (x1, y1, x2, y2) in {**teclas_blancas, **teclas_negras}.items():
                if x1 < x < x2 and y1 < y < y2:
                    tecla_presionada = nota

            # Si se detecta una nueva tecla presionada, reproducir sonido
            if tecla_presionada and tecla_presionada != tecla_anterior:
                notas[tecla_presionada].play()
                tecla_anterior = tecla_presionada
            elif tecla_presionada is None:
                tecla_anterior = None  # Resetear si no hay teclas presionadas

            # Dibujar los puntos de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        tecla_presionada = None  # Resetear si no se detectan manos

    # Mostrar la ventana
    cv2.imshow("Piano Virtual", frame)

    # Salir con la tecla 'q' o la tecla Escape
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 27 es el código ASCII para la tecla Escape
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()