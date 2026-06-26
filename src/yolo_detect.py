import os
import csv
from ultralytics import YOLO

def detect_objects(image_dir='data/raw/images', output_file='data/yolo_results.csv'):
    model = YOLO('yolov8n.pt')
    results_data = []
    
    if not os.path.exists(image_dir):
        print("No images directory found")
        return
    
    for channel in os.listdir(image_dir):
        channel_path = os.path.join(image_dir, channel)
        if not os.path.isdir(channel_path):
            continue
        for img_file in os.listdir(channel_path):
            img_path = os.path.join(channel_path, img_file)
            results = model(img_path, verbose=False)
            for r in results:
                boxes = r.boxes
                if len(boxes) > 0:
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        name = model.names[cls]
                        results_data.append({
                            'image_path': img_path,
                            'message_id': img_file.replace('.jpg', ''),
                            'channel_name': channel,
                            'detected_class': name,
                            'confidence_score': round(conf, 3)
                        })
    
    if results_data:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results_data[0].keys())
            writer.writeheader()
            writer.writerows(results_data)
        print(f"Saved {len(results_data)} detections")
    else:
        print("No objects detected")

if __name__ == '__main__':
    detect_objects()
