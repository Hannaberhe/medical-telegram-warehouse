"""Load raw JSON files into PostgreSQL raw schema."""
import json
import os

def load_json_to_postgres(data_dir='data/raw/telegram_messages'):
    """Read JSON files and print SQL insert statements."""
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                with open(os.path.join(folder_path, file)) as f:
                    messages = json.load(f)
                    print(f"Loaded {len(messages)} messages from {file}")

if __name__ == '__main__':
    load_json_to_postgres()
