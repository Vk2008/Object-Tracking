Objective: Tracking a moving object in `input_video` using Classical Computer Vision.
Tracking Method: Interactive Template Selection(Normalized Cross-Correlation Template Matching)
Flow:
- A frame ~ 1 second into the video is shown for the user to select the object(RoI).
- Each frame is matched to the template and a bounding box is drawn around the best match.
- Tracked Video and Object Trajectory Plot is saved.

Challenges Faced:
- The assumptions stated in the PS were found to be not true for the provided input video. There were issues in the distinctivity of the object from the background.
- HSV Colour-Based Tracking could not be applied as the object(kite) shared similar colours as the trees and moreover, the HSV range was not stable because of reflections, shadows, etc.
- With template matching, the first frame did not have the object hence ~1s had to be chosen. For a better tracking, the best frame from the video can be identified and used.
- To avoid False Positives, conditions were applied in form of MATCH_THRESHOLD, which also causes the tracking rectangle to be missing in some frames.
- For similar reasons, the Trajectory Plot is not clean. But it was tested for another sample video(input_video_1.mp4) and it gave satisfactory results.

Improvements:
- With the same method, Adaptive Threshold could help.
- Kalman Filter can be used to predict the next position.
- If template matching proves to be unreliable for a significant proportion of test-cases, the method can be shifted to LK Optical Flow (since I had a single test-case and created another, moving to LK Optical Flow felt not worthy.)

Submission
Date: 28 January 2026
Name: Vanshika Kataria
Entry Number: 2025PH11320