import face_recognition
import cv2
import numpy as np

def recognize_face(image_path, known_face_encodings, known_face_names):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Find all the faces in the image
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    
    # Loop through each face found in the image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Different Person"
        
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        # Draw a box around the face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Face Recognition', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Load a sample picture and learn how to recognize it
    known_image = face_recognition.load_image_file("E:\\SIH2K24\\SnapAuthExperimenting\\Passportphoto.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]
    
    # Create arrays of known face encodings and their names
    known_face_encodings = [known_encoding]
    known_face_names = ["Same Person"]
    
    # Recognize faces in a test image
    recognize_face("E:\\SIH2K24\\SnapAuthExperimenting\\NasiruddinThander.jpg", known_face_encodings, known_face_names)