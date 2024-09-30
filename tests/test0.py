

import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


cap = cv2.VideoCapture(0)


with mp_face_mesh.FaceMesh(
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(frame_rgb)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame_bgr,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                
                left_eye_landmarks = [33, 133, 145, 153, 154, 155, 159, 160, 161, 246]
                right_eye_landmarks = [362, 382, 385, 387, 388, 466, 463, 474, 475, 476]
                
                for idx in left_eye_landmarks:
                    landmark = face_landmarks.landmark[idx]
                    h, w, c = frame_bgr.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame_bgr, (x, y), 2, (0, 255, 0), -1)
                    
                for idx in right_eye_landmarks:
                    landmark = face_landmarks.landmark[idx]
                    h, w, c = frame_bgr.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame_bgr, (x, y), 2, (255, 0, 0), -1)
                    
        
        cv2.imshow('EyeTracking', frame_bgr)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()