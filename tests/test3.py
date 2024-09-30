import cv2
import mediapipe as mp
import json
import math

# Load spot data from the JSON file
with open('spot_data.json', 'r') as f:
    spot_data = json.load(f)

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Check if the eye position is following the spot
def check_eye_on_spot(eye_position, spot_data, threshold=50):
    for spot in spot_data:
        spot_pos = spot['position']
        if distance(eye_position, spot_pos) < threshold:
            return True
    return False

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        # Convert to RGB for Mediapipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(frame_rgb)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        left_eye_position = None
        right_eye_position = None

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame_bgr,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())

                # Get eye landmarks for both eyes
                left_eye_landmarks = [33, 133, 145, 153, 154, 155, 159, 160, 161, 246]
                right_eye_landmarks = [362, 382, 385, 387, 388, 466, 463, 474, 475, 476]

                # Get the average position of left eye
                left_eye_points = []
                for idx in left_eye_landmarks:
                    landmark = face_landmarks.landmark[idx]
                    h, w, c = frame_bgr.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    left_eye_points.append((x, y))
                    cv2.circle(frame_bgr, (x, y), 2, (0, 255, 0), -1)

                if left_eye_points:
                    left_eye_position = (sum([p[0] for p in left_eye_points]) // len(left_eye_points),
                                         sum([p[1] for p in left_eye_points]) // len(left_eye_points))

                # Get the average position of right eye
                right_eye_points = []
                for idx in right_eye_landmarks:
                    landmark = face_landmarks.landmark[idx]
                    h, w, c = frame_bgr.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    right_eye_points.append((x, y))
                    cv2.circle(frame_bgr, (x, y), 2, (255, 0, 0), -1)

                if right_eye_points:
                    right_eye_position = (sum([p[0] for p in right_eye_points]) // len(right_eye_points),
                                          sum([p[1] for p in right_eye_points]) // len(right_eye_points))

        # Check if eyes are following the spots
        if left_eye_position and check_eye_on_spot(left_eye_position, spot_data):
            cv2.putText(frame_bgr, "Left Eye following spot!", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if right_eye_position and check_eye_on_spot(right_eye_position, spot_data):
            cv2.putText(frame_bgr, "Right Eye following spot!", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('EyeTracking', frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
