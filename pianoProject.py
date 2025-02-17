import cv2
import mediapipe as mp
import pygame

# Inicializar pygame para los sonidos
pygame.init()

# Cargar sonidos de las notas (asegúrate de tener estos archivos en la misma carpeta)
notas = {
    # Octava 3
    "Do3": pygame.mixer.Sound("notes/c3.mp3"),
    "Re3": pygame.mixer.Sound("notes/d3.mp3"),
    "Mi3": pygame.mixer.Sound("notes/e3.mp3"),
    "Fa3": pygame.mixer.Sound("notes/f3.mp3"),
    "Sol3": pygame.mixer.Sound("notes/g3.mp3"),
    "La3": pygame.mixer.Sound("notes/a3.mp3"),
    "Si3": pygame.mixer.Sound("notes/b3.mp3"),
    
    "Do#3": pygame.mixer.Sound("notes/c-3.mp3"),
    "Re#3": pygame.mixer.Sound("notes/d-3.mp3"),
    "Fa#3": pygame.mixer.Sound("notes/f-3.mp3"),
    "Sol#3": pygame.mixer.Sound("notes/g-3.mp3"),
    "La#3": pygame.mixer.Sound("notes/a-3.mp3"),

    # Octava 4
    "Do4": pygame.mixer.Sound("notes/c4.mp3"),
    "Re4": pygame.mixer.Sound("notes/d4.mp3"),
    "Mi4": pygame.mixer.Sound("notes/e4.mp3"),
    "Fa4": pygame.mixer.Sound("notes/f4.mp3"),
    "Sol4": pygame.mixer.Sound("notes/g4.mp3"),
    "La4": pygame.mixer.Sound("notes/a4.mp3"),
    "Si4": pygame.mixer.Sound("notes/b4.mp3"),
    
    "Do#4": pygame.mixer.Sound("notes/c-4.mp3"),
    "Re#4": pygame.mixer.Sound("notes/d-4.mp3"),
    "Fa#4": pygame.mixer.Sound("notes/f-4.mp3"),
    "Sol#4": pygame.mixer.Sound("notes/g-4.mp3"),
    "La#4": pygame.mixer.Sound("notes/a-4.mp3"),

    # Octava 5
    "Do5": pygame.mixer.Sound("notes/c5.mp3"),
    "Re5": pygame.mixer.Sound("notes/d5.mp3"),
    "Mi5": pygame.mixer.Sound("notes/e5.mp3"),
    "Fa5": pygame.mixer.Sound("notes/f5.mp3"),
    "Sol5": pygame.mixer.Sound("notes/g5.mp3"),
    "La5": pygame.mixer.Sound("notes/a5.mp3"),
    "Si5": pygame.mixer.Sound("notes/b5.mp3"),
    
    "Do#5": pygame.mixer.Sound("notes/c-5.mp3"),
    "Re#5": pygame.mixer.Sound("notes/d-5.mp3"),
    "Fa#5": pygame.mixer.Sound("notes/f-5.mp3"),
    "Sol#5": pygame.mixer.Sound("notes/g-5.mp3"),
    "La#5": pygame.mixer.Sound("notes/a-5.mp3"),

    "Do#6": pygame.mixer.Sound("notes/c6.mp3"),
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
# Definir posiciones de teclas en la imagen (ajusta según tu imagen)
teclas_blancas = {
    "Do3":  (0, 170, 100, 390),  # 250 - 30 y 470 - 30
    "Re3":  (100, 170, 200, 390),
    "Mi3":  (200, 170, 300, 390),
    "Fa3":  (300, 170, 400, 390),
    "Sol3": (400, 170, 500, 390),
    "La3":  (500, 170, 600, 390),
    "Si3":  (600, 170, 700, 390),

    "Do4": (700, 170, 800, 390),
    "Re4": (800, 170, 900, 390),
    "Mi4": (900, 170, 1000, 390),
    "Fa4": (1000, 170, 1100, 390),
    "Sol4": (1100, 170, 1200, 390),
    "La4": (1200, 170, 1300, 390),
    "Si4": (1300, 170, 1400, 390),

    "Do5": (1400, 170, 1500, 390),
    "Re5": (1500, 170, 1600, 390),
    "Mi5": (1600, 170, 1700, 390),
    "Fa5": (1700, 170, 1800, 390),
    "Sol5": (1800, 170, 1900, 390),
    "La5": (1900, 170, 2000, 390),
    "Si5": (2000, 170, 2100, 390),
}

teclas_negras = {
    "Do#3": (75, 170, 125, 270),  # 250 - 30 y 350 - 30
    "Re#3": (175, 170, 225, 270),
    "Fa#3": (375, 170, 425, 270),
    "Sol#3": (475, 170, 525, 270),
    "La#3": (575, 170, 625, 270),

    "Do#4": (775, 170, 825, 270),
    "Re#4": (875, 170, 925, 270),
    "Fa#4": (1075, 170, 1125, 270),
    "Sol#4": (1175, 170, 1225, 270),
    "La#4": (1275, 170, 1325, 270),
    
    "Do#5": (1475, 170, 1525, 270),
    "Re#5": (1575, 170, 1625, 270),
    "Fa#5": (1775, 170, 1825, 270),
    "Sol#5": (1875, 170, 1925, 270),
    "La#5": (1975, 170, 2025, 270),
}

tecla_anterior = None  # Para evitar que suene muchas veces una misma tecla
tecla_presionada_izq = None  # Inicializar tecla_presionada para la mano izquierda
tecla_presionada_der = None  # Inicializar tecla_presionada para la mano derecha
tecla_anterior_izq = None  # Para evitar que suene muchas veces una misma tecla para la mano izquierda
tecla_anterior_der = None  # Para evitar que suene muchas veces una misma tecla para la mano derecha

# Definir la canción (ejemplo: "Twinkle Twinkle Little Star")
cancion = ["Do4", "Do4", "Sol4", "Sol4", "La4", "La4", "Sol4", "Fa4", "Fa4", "Mi4", "Mi4", "Re4", "Re4", "Do4"]
nombre_cancion = "Twinkle Twinkle Little Star"

# Inicializar el índice de la canción y el marcador
indice_cancion = 0
score = 0

# Variables para el menú
menu_activo = True
boton_jugar = (540, 300, 740, 400)  # Coordenadas del botón de jugar

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

    if menu_activo:
        # Dibujar el menú
        cv2.putText(frame, "Proyecto Piano Virtual", (frame_width // 2 - 300, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.rectangle(frame, (frame_width // 2 - 100, 300), (frame_width // 2 + 100, 400), (0, 255, 0), -1)
        cv2.putText(frame, "Jugar", (frame_width // 2 - 50, 370), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        # Si se detectan manos
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Obtener coordenadas del dedo índice (índice 8 en Mediapipe)
                x_tip, y_tip = int(hand_landmarks.landmark[8].x * piano_width), int(hand_landmarks.landmark[8].y * 480)
                x_base, y_base = int(hand_landmarks.landmark[7].x * piano_width), int(hand_landmarks.landmark[7].y * 480)

                # Calcular la dirección del dedo
                direction_x = x_tip - x_base
                direction_y = y_tip - y_base

                # Ajustar la posición del círculo para que esté en la punta del dedo
                x = x_tip + direction_x // 2 
                y = y_tip + direction_y // 2 + 60

                # Dibujar un círculo en la punta del dedo índice
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                # Verificar si el dedo toca el botón de jugar
                if frame_width // 2 - 100 < x < frame_width // 2 + 100 and 300 < y < 400:
                    menu_activo = False
                    break

    else:
        # Dibujar el marcador en la parte superior
        cv2.putText(frame, f"Puntaje: {score}", (10, 30), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Cancion: {nombre_cancion}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Dibujar las teclas blancas del piano con sombra y bordes curvados
        for nota, (x1, y1, x2, y2) in teclas_blancas.items():
            shadow_color = (192, 192, 192)  # Gris claro para la sombra
            border_color = (169, 169, 169)  # Plomo para el borde inferior
            color = (255, 255, 255)  # Blanco
            if tecla_presionada_izq == nota or tecla_presionada_der == nota:
                color = (169, 169, 169)  # Plomo
                shadow_color = (105, 105, 105)  # Gris oscuro para la sombra cuando se presiona
            if nota == cancion[indice_cancion]:
                color = (0, 255, 255)  # Amarillo para la tecla actual de la canción
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
            if nota == cancion[indice_cancion]:
                color = (0, 255, 255)  # Amarillo para la tecla actual de la canción
            # Dibujar sombra desde el inicio del piano
            cv2.rectangle(frame, (x1 + 5, 250), (x2 + 5, y2 + 5), shadow_color, -1)
            # Dibujar tecla
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)  # Relleno
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Borde negro

        # Si se detectan manos
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Obtener coordenadas del dedo índice (índice 8 en Mediapipe)
                x_tip = int(hand_landmarks.landmark[8].x * piano_width)
                y_tip = int(hand_landmarks.landmark[8].y * 480)
            
                # Usar directamente la punta del dedo para el círculo
                x = x_tip
                y = y_tip

                # Dibujar un círculo en la punta del dedo índice
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                # Verificar si el dedo toca alguna tecla
                if hand_landmarks.landmark[8].x < 0.5:  # Mano izquierda
                    tecla_presionada_izq = None
                    for nota, (x1, y1, x2, y2) in {**teclas_blancas, **teclas_negras}.items():
                        if x1 < x < x2 and y1 < y < y2:
                            tecla_presionada_izq = nota
                    if tecla_presionada_izq and tecla_presionada_izq != tecla_anterior_izq:
                        notas[tecla_presionada_izq].play()
                        if tecla_presionada_izq == cancion[indice_cancion]:
                            score += 1
                            indice_cancion = (indice_cancion + 1) % len(cancion)
                        tecla_anterior_izq = tecla_presionada_izq
                else:  # Mano derecha
                    tecla_presionada_der = None
                    for nota, (x1, y1, x2, y2) in {**teclas_blancas, **teclas_negras}.items():
                        if x1 < x < x2 and y1 < y < y2:
                            tecla_presionada_der = nota
                    if tecla_presionada_der and tecla_presionada_der != tecla_anterior_der:
                        notas[tecla_presionada_der].play()
                        if tecla_presionada_der == cancion[indice_cancion]:
                            score += 1
                            indice_cancion = (indice_cancion + 1) % len(cancion)
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