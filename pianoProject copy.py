import cv2
import pygame
import mediapipe as mp
import numpy as np

# Inicializar Pygame
pygame.init()
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Piano Virtual")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (100, 149, 237)  # Color de tecla presionada

# Cargar sonidos
notas = {
    "Do": pygame.mixer.Sound("do.mp3"),
    "Re": pygame.mixer.Sound("re.mp3"),
    "Mi": pygame.mixer.Sound("mi.mp3"),
    "Fa": pygame.mixer.Sound("fa.mp3"),
    "Sol": pygame.mixer.Sound("sol.mp3"),
    "La": pygame.mixer.Sound("la.mp3"),
    "Si": pygame.mixer.Sound("si.mp3"),
}

# Lista de teclas blancas y negras
teclas_blancas = [(i * 80, 400, 80, 200) for i in range(10)]
teclas_negras = [(i * 80 + 60, 400, 50, 120) for i in range(9) if i % 7 not in [2, 5]]

# Asignación de teclas a notas
teclas_piano = {
    pygame.K_a: "Do",
    pygame.K_s: "Re",
    pygame.K_d: "Mi",
    pygame.K_f: "Fa",
    pygame.K_g: "Sol",
    pygame.K_h: "La",
    pygame.K_j: "Si",
}

# Iniciar cámara con mayor resolución
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Error al abrir la cámara")

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

running = True
teclas_presionadas = set()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in teclas_piano:
                notas[teclas_piano[event.key]].play()
                teclas_presionadas.add(teclas_piano[event.key])
        elif event.type == pygame.KEYUP:
            if event.key in teclas_piano:
                teclas_presionadas.discard(teclas_piano[event.key])

    # Capturar imagen de la cámara
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Dibujar fondo de la cámara detrás del piano
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        ventana.blit(pygame.transform.scale(frame, (ANCHO_VENTANA, ALTO_VENTANA)), (0, 0))

        # Dibujar teclas blancas y negras
        for tecla in teclas_blancas:
            color = BLANCO if tecla not in teclas_presionadas else AZUL
            pygame.draw.rect(ventana, color, tecla, border_radius=5)
            pygame.draw.rect(ventana, NEGRO, tecla, 2)
        for tecla in teclas_negras:
            pygame.draw.rect(ventana, NEGRO, tecla, border_radius=5)

        # Dibujar manos y detectar interacción con teclas
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    x, y = int(lm.x * ANCHO_VENTANA), int(lm.y * ALTO_VENTANA)
                    for i, tecla in enumerate(teclas_blancas):
                        tx, ty, tw, th = tecla
                        if tx < x < tx + tw and ty < y < ty + th:
                            teclas_presionadas.add(tecla)
                            notas["Do"].play()

    pygame.display.flip()

cap.release()
pygame.quit()
