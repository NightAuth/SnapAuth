import face_recognition
import cv2
import numpy as np

def recognize_face_live(known_face_encodings, known_face_names):
    # Initialize the webcam (0 is usually the default camera index)
    video_capture = cv2.VideoCapture(0)
    
    while True:
        # Capture a single frame from the video stream
        ret, frame = video_capture.read()
        
        # Convert the frame from BGR (OpenCV's default color format) to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all the faces in the current frame of the video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Different Person"
            
            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Display the resulting frame
        cv2.imshow('Live Face Recognition', frame)
        
        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Load a sample picture and learn how to recognize it
    known_image = face_recognition.load_image_file("E:\\SIH2K24\\SnapAuthExperimenting\\Passportphoto.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]
    
    # Create arrays of known face encodings and their names
    known_face_encodings = [known_encoding]
    known_face_names = ["Same Person"]
    
    # Recognize faces from live video stream
    recognize_face_live(known_face_encodings, known_face_names)
