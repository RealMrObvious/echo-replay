import json

def load_config():
    # Load configuration from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Print the loaded configuration for debugging
    print(f"Hotkey: {config['hotkey']}")
    print(f"Output Directory: {config['output_directory']}")
    print(f"Games: {config['games']}")

    return config