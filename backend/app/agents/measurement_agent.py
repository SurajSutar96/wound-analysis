import numpy as np

class MeasurementAgent:
    def calculate_dimensions(self, mask):
        """
        Calculates physical dimensions from a binary mask.
        In a real production app, we would use a reference object (like a coin) 
        or LiDAR depth sensor data to get an accurate pixel-to-cm ratio.
        """
        # Simple bounding box for length/width
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return {"length": 0, "width": 0, "depth": 0, "area": 0, "volume": 0}
            
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        # Heuristic scaling: Assuming standard 640x640 frame at 30cm distance
        # 1 pixel ≈ 0.04 cm
        pixel_to_cm = 0.04 
        
        length = round((rmax - rmin) * pixel_to_cm, 1)
        width = round((cmax - cmin) * pixel_to_cm, 1)
        
        # Depth Estimation: Assuming depth is proportional to the square root 
        # of the area (shallow wounds usually have smaller depth relative to area)
        area_pixels = np.sum(mask)
        area_cm2 = round(area_pixels * (pixel_to_cm ** 2), 1)
        
        # Basic heuristic for depth (0.2 to 2.0 cm based on area)
        depth_cm = round(max(0.2, min(2.0, np.sqrt(area_cm2) * 0.15)), 1)
        
        volume_cm3 = round(area_cm2 * depth_cm * 0.7, 1) # 0.7 is a shape factor for ellipsoid-like wounds
        
        return {
            "length": length,
            "width": width,
            "depth": depth_cm,
            "area": area_cm2,
            "volume": volume_cm3
        }
