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
    "Re2": pygame.mixer.Sound("re.mp3"),
    "Mi2": pygame.mixer.Sound("mi.mp3"),
    "Fa2": pygame.mixer.Sound("fa.mp3"),
    "Sol2": pygame.mixer.Sound("sol.mp3"),
    "La2": pygame.mixer.Sound("la.mp3"),
    "Si2": pygame.mixer.Sound("si.mp3"),
    "Do3": pygame.mixer.Sound("do2.mp3"),
    "Do#2": pygame.mixer.Sound("re.mp3"),
    "Re#2": pygame.mixer.Sound("re.mp3"),
    "Fa#2": pygame.mixer.Sound("re.mp3"),
    "Sol#2": pygame.mixer.Sound("re.mp3"),
    "La#2": pygame.mixer.Sound("re.mp3"),
    "Re3": pygame.mixer.Sound("re.mp3"),
    "Mi3": pygame.mixer.Sound("mi.mp3"),
    "Fa3": pygame.mixer.Sound("fa.mp3"),
    "Sol3": pygame.mixer.Sound("sol.mp3"),
    "La3": pygame.mixer.Sound("la.mp3"),
    "Si3": pygame.mixer.Sound("si.mp3"),
    "Do4": pygame.mixer.Sound("do2.mp3"),
    "Do#3": pygame.mixer.Sound("re.mp3"),
    "Re#3": pygame.mixer.Sound("re.mp3"),
    "Fa#3": pygame.mixer.Sound("re.mp3"),
    "Sol#3": pygame.mixer.Sound("re.mp3"),
    "La#3": pygame.mixer.Sound("re.mp3"),
}

# Cargar la imagen del piano
piano_img = cv2.imread("piano.png")

# Ajustar el tamaño de la imagen del piano
piano_width, piano_height = 2200, 470  # Ajustar el tamaño para que se muestren todas las teclas
piano_img = cv2.resize(piano_img, (piano_width, piano_height))

# Inicializar Mediapipe para detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Iniciar captura de video
cap = cv2.VideoCapture(0)
cv2.namedWindow("Piano Virtual", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Piano Virtual", 1280, 720)  # Ajustar el tamaño de la ventana

# Centrar la ventana en la pantalla
screen_width = cv2.getWindowImageRect("Piano Virtual")[2]
screen_height = cv2.getWindowImageRect("Piano Virtual")[3]
cv2.moveWindow("Piano Virtual", (screen_width - 1280) // 2, (screen_height - 720) // 2)

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
    "Re2": (800, 250, 900, 470),
    "Mi2": (900, 250, 1000, 470),
    "Fa2": (1000, 250, 1100, 470),
    "Sol2": (1100, 250, 1200, 470),
    "La2": (1200, 250, 1300, 470),
    "Si2": (1300, 250, 1400, 470),
    "Do3": (1400, 250, 1500, 470),
    "Re3": (1500, 250, 1600, 470),
    "Mi3": (1600, 250, 1700, 470),
    "Fa3": (1700, 250, 1800, 470),
    "Sol3": (1800, 250, 1900, 470),
    "La3": (1900, 250, 2000, 470),
    "Si3": (2000, 250, 2100, 470),
    "Do4": (2100, 250, 2200, 470),
}

teclas_negras = {
    "Do#": (75, 250, 125, 350),
    "Re#": (175, 250, 225, 350),
    "Fa#": (375, 250, 425, 350),
    "Sol#": (475, 250, 525, 350),
    "La#": (575, 250, 625, 350),
    "Do#2": (875, 250, 925, 350),
    "Re#2": (975, 250, 1025, 350),
    "Fa#2": (1175, 250, 1225, 350),
    "Sol#2": (1275, 250, 1325, 350),
    "La#2": (1375, 250, 1425, 350),
    "Do#3": (1575, 250, 1625, 350),
    "Re#3": (1675, 250, 1725, 350),
    "Fa#3": (1875, 250, 1925, 350),
    "Sol#3": (1975, 250, 2025, 350),
    "La#3": (2075, 250, 2125, 350),
}

tecla_anterior = None  # Para evitar que suene muchas veces una misma tecla
tecla_presionada_izq = None  # Inicializar tecla_presionada para la mano izquierda
tecla_presionada_der = None  # Inicializar tecla_presionada para la mano derecha
tecla_anterior_izq = None  # Para evitar que suene muchas veces una misma tecla para la mano izquierda
tecla_anterior_der = None  # Para evitar que suene muchas veces una misma tecla para la mano derecha

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Espejar la imagen para que sea más intuitivo
    frame = cv2.flip(frame, 1)

    # Obtener tamaño del video
    frame_height, frame_width, _ = frame.shape
    frame = cv2.resize(frame, (piano_width, 720))  # Ajustar el tamaño del frame para que se muestren todas las teclas

    # Convertir la imagen a RGB para Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Dibujar las teclas blancas del piano con sombra y bordes curvados
    for nota, (x1, y1, x2, y2) in teclas_blancas.items():
        shadow_color = (192, 192, 192)  # Gris claro para la sombra
        border_color = (169, 169, 169)  # Plomo para el borde inferior
        color = (255, 255, 255)  # Blanco
        if tecla_presionada_izq == nota or tecla_presionada_der == nota:
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
        if tecla_presionada_izq == nota or tecla_presionada_der == nota:
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
            if hand_landmarks.landmark[8].x < 0.5:  # Mano izquierda
                tecla_presionada_izq = None
                for nota, (x1, y1, x2, y2) in {**teclas_blancas, **teclas_negras}.items():
                    if x1 < x < x2 and y1 < y < y2:
                        tecla_presionada_izq = nota
                if tecla_presionada_izq and tecla_presionada_izq != tecla_anterior_izq:
                    notas[tecla_presionada_izq].play()
                    tecla_anterior_izq = tecla_presionada_izq
            else:  # Mano derecha
                tecla_presionada_der = None
                for nota, (x1, y1, x2, y2) in {**teclas_blancas, **teclas_negras}.items():
                    if x1 < x < x2 and y1 < y < y2:
                        tecla_presionada_der = nota
                if tecla_presionada_der and tecla_presionada_der != tecla_anterior_der:
                    notas[tecla_presionada_der].play()
                    tecla_anterior_der = tecla_presionada_der

            # Dibujar los puntos de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        tecla_presionada_izq = None  # Resetear si no se detectan manos
        tecla_presionada_der = None  # Resetear si no se detectan manos

    # Resetear tecla_anterior si ninguna tecla está siendo presionada
    if tecla_presionada_izq is None and tecla_presionada_der is None:
        tecla_anterior_izq = None
        tecla_anterior_der = None

    # Mostrar la ventana en tamaño ajustado
    cv2.imshow("Piano Virtual", frame)

    # Salir con la tecla 'q', la tecla Escape o al cerrar la ventana
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27 or cv2.getWindowProperty("Piano Virtual", cv2.WND_PROP_VISIBLE) < 1:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()