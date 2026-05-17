# About the project
A real-time driver monitoring system that detects drowsiness using computer vision and fuzzy logic.
Instead of using fixed thresholds, the system applies fuzzy reasoning to evaluate eye states and produce gradual risk levels (Safe, Warning, Danger).
The system is lightweight, explainable, and suitable for real-world uncertain driving conditions.

# Main Idea
The main goal of this system is to simulate human-like reasoning when evaluating driver alertness.
Instead of making a strict decision like:

If EAR < threshold → drowsy
The system evaluates eye behavior gradually and assigns a risk level based on degrees of uncertainty.
This is achieved using fuzzy logic.

# What's Fuzzy logic?

Fuzzy Logic is a mathematical reasoning approach that allows partial truth values between 0 and 1 instead of binary decisions (0 or 1).

In this project:
Eye state is not simply “open” or “closed”
It can be partially open with different degrees
Risk is not fixed, but gradually inferred

This makes the system more realistic for noisy and uncertain environments like driving.

# Feature Extraction (EAR)

The system uses Eye Aspect Ratio (EAR) as the main feature extracted from facial landmarks detected by MediaPipe.

EAR measures: Eye openness using geometric distances between landmark points.

EAR=
2∥p
1
	​

−p
4
	​

∥
∥p
2
	​

−p
6
	​

∥+∥p
3
	​

−p
5
	​

∥
	​


Interpretation:
High EAR → eyes open
Medium EAR → partially open
Low EAR → eyes closed
