from pose_detection import process_image


# =========================
# STANCE ASSESSMENT
# =========================
def calculate_stance(landmarks):

    left_ankle = landmarks[27]
    right_ankle = landmarks[28]

    stance_width = abs(left_ankle.x - right_ankle.x)

    if 0.15 <= stance_width <= 0.35:
        return 100, "Excellent batting stance"
    elif 0.10 <= stance_width <= 0.45:
        return 80, "Good stance, minor improvement needed"
    else:
        return 60, "Stance width needs improvement"


# =========================
# BALANCE ASSESSMENT
# =========================
def calculate_balance(landmarks):

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    shoulder_diff = abs(
        left_shoulder.y - right_shoulder.y
    )

    if shoulder_diff < 0.03:
        return 100, "Excellent balance"
    elif shoulder_diff < 0.08:
        return 80, "Slight imbalance detected"
    else:
        return 60, "Poor balance"


# =========================
# FOOTWORK ASSESSMENT
# =========================
def calculate_footwork(landmarks):

    left_knee = landmarks[25]
    right_knee = landmarks[26]

    knee_diff = abs(
        left_knee.x - right_knee.x
    )

    if knee_diff > 0.15:
        return 100, "Excellent footwork"
    elif knee_diff > 0.08:
        return 80, "Good foot movement"
    else:
        return 60, "Footwork needs improvement"


# =========================
# OVERALL SCORE
# =========================
def overall_score(stance, balance, footwork):

    return round(
        (stance + balance + footwork) / 3,
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
# MAIN PROGRAM
# =========================
if __name__ == "__main__":

    image_path = input(
        "Enter image path: "
    ).strip()

    landmarks = process_image(image_path)

    print("\nLandmarks returned:",
          landmarks is not None)

    if landmarks is None:
        print("❌ Pose detection failed")
        exit()

    # ---------------------
    # Calculate Scores
    # ---------------------
    stance_score, stance_feedback = \
        calculate_stance(landmarks)

    balance_score, balance_feedback = \
        calculate_balance(landmarks)

    footwork_score, footwork_feedback = \
        calculate_footwork(landmarks)

    total_score = overall_score(
        stance_score,
        balance_score,
        footwork_score
    )

    rating = performance_rating(
        total_score
    )

    # ---------------------
    # REPORT
    # ---------------------
    print("\n")
    print("=" * 45)
    print("🏏 BATSMAN AI ASSESSMENT REPORT")
    print("=" * 45)

    print(
        f"\nStance Score   : {stance_score}/100"
    )
    print(
        f"Feedback       : {stance_feedback}"
    )

    print(
        f"\nBalance Score  : {balance_score}/100"
    )
    print(
        f"Feedback       : {balance_feedback}"
    )

    print(
        f"\nFootwork Score : {footwork_score}/100"
    )
    print(
        f"Feedback       : {footwork_feedback}"
    )

    print("\n" + "-" * 45)

    print(
        f"Overall Score  : {total_score}/100"
    )

    print(
        f"Performance    : {rating}"
    )

    print("-" * 45)