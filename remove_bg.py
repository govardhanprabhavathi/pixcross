import cv2
import numpy as np
import glob

print("Processing 145 frames to remove background noise...")
files = glob.glob('images/frames_ani/pixxframes_*.png')
for f in files:
    img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    
    # Ensure it has an alpha channel
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Calculate brightness based on max RGB value
    brightness = np.max(img[:,:,:3], axis=2)
    
    # Smooth thresholding to kill dark background noise but keep the bright glassy shape
    # Any noise below RGB 15 becomes completely transparent
    # Smoothly blends into full opacity by RGB 40 to avoid jagged edges
    alpha = np.clip((brightness.astype(np.float32) - 15) / 25.0 * 255, 0, 255).astype(np.uint8)
    
    img[:,:,3] = alpha
    
    cv2.imwrite(f, img)

print("Done processing!")
