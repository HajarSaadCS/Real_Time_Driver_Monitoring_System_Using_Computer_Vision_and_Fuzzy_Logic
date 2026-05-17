import cv2
import mediapipe as mp
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import winsound
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# 🔹 Eye points
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def eye_aspect_ratio(landmarks, eye_points, image_w, image_h):
    points = []

    for idx in eye_points:
        x = int(landmarks[idx].x * image_w)
        y = int(landmarks[idx].y * image_h)
        points.append((x, y))

    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

    return (A + B) / (2.0 * C)

ear_var = ctrl.Antecedent(np.arange(0, 0.5, 0.01), 'ear')
risk = ctrl.Consequent(np.arange(0, 1, 0.01), 'risk')

ear_var['low'] = fuzz.trimf(ear_var.universe, [0, 0, 0.15])
ear_var['medium'] = fuzz.trimf(ear_var.universe, [0.1, 0.2, 0.3])
ear_var['high'] = fuzz.trimf(ear_var.universe, [0.25, 0.5, 0.5])

risk['low'] = fuzz.trimf(risk.universe, [0, 0, 0.4])
risk['medium'] = fuzz.trimf(risk.universe, [0.3, 0.5, 0.7])
risk['high'] = fuzz.trimf(risk.universe, [0.6, 1, 1])

rule1 = ctrl.Rule(ear_var['high'], risk['low'])
rule2 = ctrl.Rule(ear_var['medium'], risk['medium'])
rule3 = ctrl.Rule(ear_var['low'], risk['high'])

risk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)

last_beep = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS
            )

            
            ear_value = eye_aspect_ratio(
                face_landmarks.landmark,
                LEFT_EYE,
                w,
                h
            )

            risk_sim.input['ear'] = ear_value
            risk_sim.compute()
            risk_value = risk_sim.output['risk']

            if risk_value < 0.4:
                status = "Safe"
                color = (0, 255, 0)

            elif risk_value < 0.75:
                status = "Warning"
                color = (0, 255, 255)

            else:
                status = "Danger"
                color = (0, 0, 255)

                # 🔊 controlled alert
                if time.time() - last_beep > 2:
                    winsound.Beep(1000, 200)
                    last_beep = time.time()

            cv2.putText(frame, f"EAR: {round(ear_value, 2)}",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2)

            cv2.putText(frame, f"Risk: {round(risk_value, 2)}",
                        (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2)

            cv2.putText(frame, f"Status: {status}",
                        (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        color,
                        2)

    cv2.imshow("Fuzzy Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
face_mesh.close()
cv2.destroyAllWindows()