import cv2
import numpy as np
import uuid
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def auto_align_images(images):
    """
    Auto-align using MTB (Median Threshold Bitmap)
    This is used in HDR pipelines to align exposures
    even when brightness/exposure differs significantly.
    """

    try:
        # Convert all images to grayscale for robust alignment
        gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]

        # Create MTB aligner
        alignMTB = cv2.createAlignMTB()
        alignMTB.setMaxBits(6)  
        alignMTB.setExcludedRange(10)  

        # Align images in place
        alignMTB.process(images, images)

        print("Auto-alignment success using MTB.")

    except Exception as e:
        print("Auto alignment failed:", e)

    return images



def process_hdr(images):

    # Step 1: Auto Alignment first
    images = auto_align_images(images)

    # Step 2: Exposure Fusion (Mertens)
    merge_mertens = cv2.createMergeMertens()
    hdr = merge_mertens.process(images)
    hdr_8bit = np.clip(hdr * 255, 0, 255).astype("uint8")

    file_id = str(uuid.uuid4())

    hdr_file = f"hdr_{file_id}.jpg"
    hist_file = f"hist_{file_id}.png"
    compare_file = f"compare_{file_id}.jpg"

    hdr_path = f"{OUTPUT_DIR}/{hdr_file}"
    hist_path = f"{OUTPUT_DIR}/{hist_file}"
    compare_path = f"{OUTPUT_DIR}/{compare_file}"

    # Save HDR
    cv2.imwrite(hdr_path, hdr_8bit)

    # Side-by-side comparison
    orig_resized = cv2.resize(images[1], (400, 300))
    hdr_resized = cv2.resize(hdr_8bit, (400, 300))
    side_by_side = np.hstack([orig_resized, hdr_resized])
    cv2.imwrite(compare_path, side_by_side)

    # Histogram
    plt.figure(figsize=(8, 4))
    plt.title("Histogram Before vs After")
    plt.hist(images[1].ravel(), bins=256, alpha=0.5, label="Original")
    plt.hist(hdr_8bit.ravel(), bins=256, alpha=0.5, label="HDR")
    plt.legend()
    plt.savefig(hist_path)
    plt.close()

    return (
        f"outputs/{hdr_file}",
        f"outputs/{hist_file}",
        f"outputs/{compare_file}"
    )
