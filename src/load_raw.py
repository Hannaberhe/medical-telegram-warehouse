"""Load raw JSON into PostgreSQL with error handling."""
import json
import os

def load_json_to_postgres(data_dir='data/raw/telegram_messages'):
    """Read JSON files and print SQL for PostgreSQL insert."""
    try:
        for folder in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder)
            if not os.path.isdir(folder_path):
                continue
            for file in os.listdir(folder_path):
                if file.endswith('.json'):
                    filepath = os.path.join(folder_path, file)
                    try:
                        with open(filepath) as f:
                            messages = json.load(f)
                        print(f"Loaded {len(messages)} from {file}")
                        for msg in messages[:3]:
                            print(f"  INSERT: {msg['message_id']} - {msg['channel_name']}")
                    except Exception as e:
                        print(f"Error reading {filepath}: {e}")
    except FileNotFoundError:
        print("Data directory not found. Run scraper first.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    load_json_to_postgres()
