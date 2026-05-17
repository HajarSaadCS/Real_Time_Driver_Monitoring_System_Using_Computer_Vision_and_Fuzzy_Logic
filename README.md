# About the Project

A real-time driver monitoring system that detects drowsiness using computer vision and fuzzy logic.

Instead of using fixed thresholds, the system applies fuzzy reasoning to evaluate eye states and produce gradual risk levels: Safe, Warning, Danger. The system is lightweight, explainable, and suitable for real-world uncertain driving conditions.


# Main Idea

The main goal of this system is to simulate human-like reasoning when evaluating driver alertness.

Instead of making a strict decision such as:

IF EAR < threshold → drowsy

The system evaluates eye behavior gradually and assigns a risk level based on uncertainty. This is achieved using fuzzy logic.


# What is Fuzzy Logic

Fuzzy Logic is a mathematical reasoning approach that allows partial truth values between 0 and 1 instead of binary decisions.

In this project:
- Eye state is not only open or closed.
- It can be partially open with different degrees.
- Risk is inferred gradually instead of being fixed.

This makes the system more suitable for real-world uncertain environments such as driving.

# Feature Extraction (EAR)
The system uses Eye Aspect Ratio (EAR) extracted from facial landmarks detected by MediaPipe. EAR measures eye openness using geometric distances between landmark points.

# EAR Formula
$EAR = \frac{|p_2 - p_6| + |p_3 - p_5|}{2 |p_1 - p_4|}$


**General Definition**  
Eye Aspect Ratio (EAR) is a geometric ratio used to measure eye openness based on facial landmarks.  
It is a scale-invariant metric, meaning it is independent of face size and camera distance.


**Landmark Points Definition**  
- p1, p4:
  - Eye corner landmarks
  - Represent the horizontal eye width
  - Used for normalization

- p2, p6:
  - Vertical eyelid landmarks (first pair)
  - Measure vertical eye opening

- p3, p5:
  - Vertical eyelid landmarks (second pair)
  - Improve stability and reduce noise sensitivity


 **Mathematical Structure**
- Numerator:
  - Sum of vertical eye distances
  - Represents eye opening height

- Denominator:
  - Horizontal eye width
  - Used for normalization

- Absolute value:
  - Ensures all distance values are positive


**Geometric Interpretation**

- EAR increases when the eye opens
- EAR decreases when the eye closes
- Provides a continuous representation of eye state


**Final Interpretation**

- High EAR:
  - Eye is open

- Medium EAR:
  - Partially open eye

- Low EAR:
  - Eye is closed

# Interpretation

High EAR means eyes are open
Medium EAR means partially open
Low EAR means eyes are closed


# Membership Functions

Each EAR value is mapped into fuzzy sets using membership functions.

**Input Variable:** EAR

Range: [0, 0.5]

-LOW means eyes closed
-MEDIUM means partially open
-HIGH means eyes open

**Output Variable:** Risk

Range: [0, 1]

-LOW means Safe
-MEDIUM means Warning
-HIGH means Danger

**Concept:**

Instead of assigning one label, each input belongs to multiple fuzzy sets with different degrees of membership between 0 and 1.

**Example:**

EAR = 0.18 may belong partially to LOW and MEDIUM at the same time.


# Fuzzy Rule Base

The system uses a Mamdani fuzzy inference system.

**Rules:**

- IF EAR is HIGH THEN Risk is LOW

- IF EAR is MEDIUM THEN Risk is MEDIUM

- IF EAR is LOW THEN Risk is HIGH

**Rule Design Logic:**

1. More open eyes correspond to lower risk
2. Closed eyes correspond to higher risk
3. Partial openness corresponds to uncertainty


# Explainable AI and Rule Transparency

Explainable AI is achieved because every decision is fully traceable to fuzzy rules. Unlike black box models, this system is fully interpretable.

**Why this system is explainable:**
-Each output is directly generated from rules
-Membership functions define input interpretation
-Inference process is fully transparent

**Relationship between rules and explainability:**
The fuzzy rule base acts as the explanation mechanism of the system.

Each decision can be traced back to:
-Which rule fired
-How strongly it was activated
-How it contributed to final risk

If the system outputs Danger:
-EAR is low
-Rule LOW leads to HIGH risk is activated
-Final risk increases accordingly

