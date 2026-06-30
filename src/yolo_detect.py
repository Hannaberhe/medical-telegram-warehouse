"""YOLOv8 object detection for Telegram images."""
import os
import csv
from ultralytics import YOLO

MODEL_NAME = 'yolov8n.pt'

def classify_image(detected_classes):
    """Classify image into promotional, product_display, lifestyle, or other."""
    has_person = 'person' in detected_classes
    has_product = any(c in detected_classes for c in ['bottle', 'cup', 'bowl', 'vase', 'wine glass'])
    
    if has_person and has_product:
        return 'promotional'
    elif has_product and not has_person:
        return 'product_display'
    elif has_person and not has_product:
        return 'lifestyle'
    else:
        return 'other'

def detect_objects(image_dir='data/raw/images', output_file='data/yolo_results.csv'):
    """Run YOLOv8 nano model on downloaded images."""
    print(f"Loading YOLOv8 model: {MODEL_NAME}")
    model = YOLO(MODEL_NAME)
    results_data = []
    
    if not os.path.exists(image_dir):
        print(f"Image directory not found: {image_dir}")
        print("Run the scraper first to download images")
        return
    
    image_count = 0
    for channel in os.listdir(image_dir):
        channel_path = os.path.join(image_dir, channel)
        if not os.path.isdir(channel_path):
            continue
        
        for img_file in os.listdir(channel_path):
            if not img_file.endswith('.jpg'):
                continue
            
            img_path = os.path.join(channel_path, img_file)
            image_count += 1
            
            try:
                results = model(img_path, verbose=False)
                
                detected_classes = []
                for r in results:
                    boxes = r.boxes
                    if len(boxes) > 0:
                        for box in boxes:
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            name = model.names[cls]
                            detected_classes.append(name)
                            results_data.append({
                                'message_id': img_file.replace('.jpg', ''),
                                'channel_name': channel,
                                'detected_class': name,
                                'confidence_score': round(conf, 3),
                                'image_category': classify_image([name])
                            })
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    
    if results_data:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['message_id', 'channel_name', 'detected_class', 'confidence_score', 'image_category'])
            writer.writeheader()
            writer.writerows(results_data)
        print(f"Processed {image_count} images")
        print(f"Saved {len(results_data)} detections to {output_file}")
    else:
        print(f"No objects detected in {image_count} images")

if __name__ == '__main__':
    detect_objects()
