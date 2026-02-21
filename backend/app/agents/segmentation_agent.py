# import torch
import numpy as np
import os
# from PIL import Image
# from ultralytics import YOLO   # ❌ YOLO disabled

class SegmentationAgent:
    def __init__(self, model_path="C:/Users/hp/Desktop/wound_analysis/backend/weight/yolo26s-seg.pt"):
        # Adjusting to handle both local and absolute path provided by user
        if not os.path.isabs(model_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.model_path = os.path.join(base_dir, model_path)
        else:
            self.model_path = model_path
            
        self.model = None

        # ❌ YOLO model loading disabled
        # try:
        #     if os.path.exists(self.model_path):
        #         self.model = YOLO(self.model_path)
        #         print(f"--- YOLO Model loaded from {self.model_path} ---")
        #     else:
        #         print(f"--- WARNING: Model not found at {self.model_path} ---")
        # except Exception as e:
        #     print(f"Error loading model: {e}")

        print("--- YOLO Disabled: Running in dummy segmentation mode ---")

    def segment(self, image_path):
        """
        Dummy segmentation function (YOLO disabled).
        Always returns a white mask and detection_success=False.
        """

        # ❌ YOLO inference disabled
        # if self.model is None:
        #     print("--- Using dummy mask (Model not loaded) ---")
        #     return np.ones((640, 640), dtype=np.uint8), False

        # try:
        #     results = self.model(image_path)
        #     result = results[0]
        #     
        #     if result.masks is not None:
        #         mask = result.masks.data[0].cpu().numpy()
        #         mask = (mask > 0.5).astype(np.uint8)
        #         return mask, True
        #     else:
        #         print("--- No wound detected by YOLO ---")
        #         return np.zeros((640, 640), dtype=np.uint8), False
        # except Exception as e:
        #     print(f"Segmentation error: {e}")
        #     return np.zeros((640, 640), dtype=np.uint8), False

        print("--- Returning dummy mask (YOLO not available) ---")
        return np.ones((640, 640), dtype=np.uint8), False