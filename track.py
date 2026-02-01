import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

VIDEO_PATH = "input_video.mp4"
OUTPUT_VIDEO = "tracked_output.mp4"
PATH_IMAGE = "trajectory.png"

DISPLAY_WIDTH = 900
MATCH_THRESHOLD = 0.65
METHOD = cv2.TM_CCOEFF_NORMED

def select_template(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(1 * fps))

    ret, frame = cap.read()
    cap.release()

    h, w = frame.shape[:2]

    scale = DISPLAY_WIDTH / w
    display_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

    roi_disp = cv2.selectROI("Select Template", display_frame, False, False)
    cv2.destroyAllWindows()

    if roi_disp == (0, 0, 0, 0):
        raise RuntimeError("No ROI selected")

    x_d, y_d, w_d, h_d = roi_disp
    x = int(x_d / scale)
    y = int(y_d / scale)
    w_roi = int(w_d / scale)
    h_roi = int(h_d / scale)

    template = frame[y:y + h_roi, x:x + w_roi]
    return template


def track_object(video_path, template):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

    trajectory = []
    global frame_idx
    frame_idx = 0

    t_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    th, tw = t_gray.shape[:2]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame_gray, t_gray, METHOD)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > MATCH_THRESHOLD:
            top_left = max_loc
            center = (top_left[0] + tw // 2, top_left[1] + th // 2)
            trajectory.append(center)

            cv2.rectangle(
                frame,
                top_left,
                (top_left[0] + tw, top_left[1] + th),
                (0, 255, 0),
                2
            )
            cv2.circle(frame, center, 4, (0, 0, 255), -1)

        out.write(frame)

        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

        frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return trajectory


def save_trajectory_image(trajectory):
    if not trajectory:
        print("No trajectory points to plot")
        return

    xs, ys = zip(*trajectory)

    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, marker="o", linewidth=2)
    plt.gca().invert_yaxis()
    plt.title("Object Trajectory")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.savefig(PATH_IMAGE, dpi=200)
    plt.close()


if __name__ == "__main__":
    template = select_template(VIDEO_PATH)
    trajectory = track_object(VIDEO_PATH, template)
    save_trajectory_image(trajectory)
    print(f'Total frames processed: {frame_idx}')