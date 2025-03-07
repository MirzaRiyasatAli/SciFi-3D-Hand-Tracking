# import cv2
# import mediapipe as mp
# import numpy as np
# import glfw
# from OpenGL.GL import *
# from OpenGL.GLU import *
# import threading
# import math
#
# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
#
# # Global variable to store hand landmarks for multiple hands
# hand_landmarks_list = []
#
# def capture_hand():
#     """Capture hand landmarks from webcam with a larger window."""
#     global hand_landmarks_list
#     cap = cv2.VideoCapture(0)
#
#     # Set higher resolution (adjust values based on your webcam's capability)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#
#     cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)  # Allow window resizing
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame = cv2.flip(frame, 1)  # Mirror effect
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = hands.process(rgb_frame)
#
#         hand_landmarks_list = []  # Reset landmarks each frame
#
#         if results.multi_hand_landmarks:
#             for hand in results.multi_hand_landmarks:
#                 hand_landmarks = [(lm.x - 0.5, -(lm.y - 0.5), -lm.z) for lm in hand.landmark]
#                 hand_landmarks_list.append(hand_landmarks)
#
#         # Resize frame before showing (adjust size as needed)
#         frame = cv2.resize(frame, (1280, 720))
#
#         cv2.imshow("Hand Tracking", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
# def draw_cylinder(p1, p2, radius=0.01, slices=16, stacks=1):
#     """Draw a cylinder (bone) from point p1 to p2."""
#     dx, dy, dz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
#     length = math.sqrt(dx**2 + dy**2 + dz**2)
#     if length == 0:
#         return
#
#     angle = math.degrees(math.acos(dz / length)) if length != 0 else 0
#     rx, ry, rz = -dy, dx, 0.0
#
#     norm = math.sqrt(rx**2 + ry**2 + rz**2)
#     if norm != 0:
#         rx /= norm
#         ry /= norm
#         rz /= norm
#
#     glPushMatrix()
#     glTranslatef(p1[0], p1[1], p1[2])
#     if norm != 0:
#         glRotatef(angle, rx, ry, rz)
#     quadric = gluNewQuadric()
#     gluCylinder(quadric, radius, radius, length, slices, stacks)
#     gluDeleteQuadric(quadric)
#     glPopMatrix()
#
#
# def draw_sphere(pos, radius=0.02, slices=16, stacks=16):
#     """Draw a sphere (joint) at the given position."""
#     glPushMatrix()
#     glTranslatef(pos[0], pos[1], pos[2])
#     quadric = gluNewQuadric()
#     gluSphere(quadric, radius, slices, stacks)
#     gluDeleteQuadric(quadric)
#     glPopMatrix()
#
#
# def draw_hand_boundary(hand_landmarks):
#     """Draw the hand boundary for a single hand."""
#     if len(hand_landmarks) < 21:
#         return
#
#     boundary_connections = [
#         (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
#         (0, 5), (5, 6), (6, 7), (7, 8),  # Index
#         (9, 10), (10, 11), (11, 12),  # Middle
#         (13, 14), (14, 15), (15, 16),  # Ring
#         (17, 18), (18, 19), (19, 20),  # Little
#         (17, 13), (13, 9), (9, 5), (5, 1),  # Palm
#         (0, 1), (0, 5), (0, 9), (0, 13), (0, 17)  # Wrist
#     ]
#
#     for idx1, idx2 in boundary_connections:
#         if idx1 < len(hand_landmarks) and idx2 < len(hand_landmarks):
#             draw_cylinder(hand_landmarks[idx1], hand_landmarks[idx2], radius=0.015)
#
#
# def draw_hand_skeleton():
#     """Render both hands' skeletons with sci-fi styling."""
#     glClearColor(0.0, 0.0, 0.1, 1.0)
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     gluLookAt(0, 0, 1.5, 0, 0, 0, 0, 1, 0)
#
#     glEnable(GL_BLEND)
#     glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#
#     # Render each hand separately
#     for hand_landmarks in hand_landmarks_list:
#         glColor4f(0.3, 0.3, 0.5, 0.4)  # Transparent bone color
#         draw_hand_boundary(hand_landmarks)
#
#         glDisable(GL_LIGHTING)
#         glColor3f(0.0, 0.8, 1.0)  # Glow effect for joints
#         for lm in hand_landmarks:
#             draw_sphere(lm, radius=0.025)
#         glEnable(GL_LIGHTING)
#
#     glDisable(GL_BLEND)
#     glfw.swap_buffers(window)
#
#
# def main():
#     global window
#     if not glfw.init():
#         return
#
#     window = glfw.create_window(1920, 1080, "Sci-Fi Hand Skeleton (Dual Hand)", None, None)
#
#     if not window:
#         glfw.terminate()
#         return
#
#     glfw.make_context_current(window)
#     glEnable(GL_DEPTH_TEST)
#     glEnable(GL_LIGHTING)
#     glEnable(GL_LIGHT0)
#     glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
#     glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
#     glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
#     glMaterialf(GL_FRONT, GL_SHININESS, 50)
#
#     glMatrixMode(GL_PROJECTION)
#     gluPerspective(45, (1920 / 1080), 0.1, 10)
#     glMatrixMode(GL_MODELVIEW)
#
#     threading.Thread(target=capture_hand, daemon=True).start()
#
#     while not glfw.window_should_close(window):
#         draw_hand_skeleton()
#         glfw.poll_events()
#
#     glfw.terminate()
#
#
# if __name__ == "__main__":
#     main()