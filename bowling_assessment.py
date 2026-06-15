from pose_detection import process_image
import math


# =========================
# ANGLE CALCULATION
# =========================
def calculate_angle(a, b, c):

    angle = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x)
        - math.atan2(a.y - b.y, a.x - b.x)
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


# =========================
# BOWLING ARM SCORE
# =========================
def bowling_arm_score(landmarks):

    right_shoulder = landmarks[12]
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]

    angle = calculate_angle(
        right_shoulder,
        right_elbow,
        right_wrist
    )

    if angle >= 165:
        return 100, angle, "Excellent bowling arm action"
    elif angle >= 150:
        return 80, angle, "Good bowling arm action"
    else:
        return 60, angle, "Arm action needs improvement"


# =========================
# FRONT KNEE SCORE
# =========================
def front_knee_score(landmarks):

    right_hip = landmarks[24]
    right_knee = landmarks[26]
    right_ankle = landmarks[28]

    angle = calculate_angle(
        right_hip,
        right_knee,
        right_ankle
    )

    if 140 <= angle <= 180:
        return 100, angle, "Excellent front knee position"
    elif 120 <= angle <= 180:
        return 80, angle, "Good knee position"
    else:
        return 60, angle, "Front knee needs improvement"


# =========================
# BODY ALIGNMENT SCORE
# =========================
def body_alignment_score(landmarks):

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    diff = abs(
        left_shoulder.y -
        right_shoulder.y
    )

    if diff < 0.03:
        return 100, "Excellent body alignment"
    elif diff < 0.08:
        return 80, "Slight body tilt detected"
    else:
        return 60, "Poor body alignment"


# =========================
# OVERALL SCORE
# =========================
def overall_score(
        arm_score,
        knee_score,
        alignment_score):

    return round(
        (
            arm_score +
            knee_score +
            alignment_score
        ) / 3,
        2
    )


# =========================
# PERFORMANCE RATING
# =========================
def performance_rating(score):

    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Average"
    else:
        return "Needs Improvement"


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    image_path = input(
        "Enter bowling image path: "
    ).strip()

    landmarks = process_image(image_path)

    print(
        "\nLandmarks returned:",
        landmarks is not None
    )

    if landmarks is None:
        print("❌ Pose detection failed")
        exit()

    arm_score, arm_angle, arm_feedback = \
        bowling_arm_score(landmarks)

    knee_score, knee_angle, knee_feedback = \
        front_knee_score(landmarks)

    alignment_score, alignment_feedback = \
        body_alignment_score(landmarks)

    total_score = overall_score(
        arm_score,
        knee_score,
        alignment_score
    )

    rating = performance_rating(
        total_score
    )

    print("\n")
    print("=" * 45)
    print("🎳 BOWLING AI ASSESSMENT REPORT")
    print("=" * 45)

    print(
        f"\nBowling Arm Score : {arm_score}/100"
    )
    print(
        f"Arm Angle         : {arm_angle:.2f}°"
    )
    print(
        f"Feedback          : {arm_feedback}"
    )

    print(
        f"\nFront Knee Score  : {knee_score}/100"
    )
    print(
        f"Knee Angle        : {knee_angle:.2f}°"
    )
    print(
        f"Feedback          : {knee_feedback}"
    )

    print(
        f"\nAlignment Score   : {alignment_score}/100"
    )
    print(
        f"Feedback          : {alignment_feedback}"
    )

    print("\n" + "-" * 45)

    print(
        f"Overall Score     : {total_score}/100"
    )

    print(
        f"Performance       : {rating}"
    )

    print("-" * 45)