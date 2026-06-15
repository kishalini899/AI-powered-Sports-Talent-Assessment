import cv2
import mediapipe as mp

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)


def detect_pose(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return pose.process(rgb)


def brighten_image(img):
    return cv2.convertScaleAbs(img, alpha=1.2, beta=30)


def resize_image(img, max_width=1280):
    h, w = img.shape[:2]

    if w > max_width:
        scale = max_width / w
        img = cv2.resize(
            img,
            (int(w * scale), int(h * scale))
        )

    return img


def is_upside_down(landmarks):
    nose_y = landmarks[mp_pose.PoseLandmark.NOSE].y

    left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
    right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y

    hip_y = (left_hip_y + right_hip_y) / 2

    return nose_y > hip_y


def process_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found")
        return None

    image = resize_image(image)

    print("Trying original image...")
    result = detect_pose(image)

    # Try brighter version
    if not result.pose_landmarks:
        print("Trying enhanced brightness...")
        enhanced = brighten_image(image)
        result = detect_pose(enhanced)

        if result.pose_landmarks:
            image = enhanced

    # Try 180° rotation
    if not result.pose_landmarks:
        print("Trying rotated image...")
        rotated = cv2.rotate(image, cv2.ROTATE_180)
        result = detect_pose(rotated)

        if result.pose_landmarks:
            image = rotated

    if not result.pose_landmarks:
        print("❌ Pose not detected after all attempts")
        return None

    print("✅ Pose detected")

    landmarks = result.pose_landmarks.landmark

    # Orientation correction
    if is_upside_down(landmarks):

        print("🔄 Upside-down detected")

        image = cv2.rotate(image, cv2.ROTATE_180)

        result = detect_pose(image)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

    mp_drawing.draw_landmarks(
        image,
        result.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    cv2.imshow("Pose Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return landmarks


if __name__ == "__main__":

    image_path = input("Enter image path: ").strip()

    landmarks = process_image(image_path)

    if landmarks is not None:
        print("✅ Landmarks extracted successfully")
    else:
        print("❌ Failed to extract landmarks")