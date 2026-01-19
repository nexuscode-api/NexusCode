import yaml
import sys
import os

# Adjust path to import modules easily
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nexus.core.rotator import KeyRotator
from nexus.core.engine import NexusEngine
from nexus.ui.display import Interface

def load_settings():
    """Loads global app settings."""
    try:
        with open('config/settings.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Creating default...")
        return {"app": {"version": "0.1.0"}, "network": {}}

def main():
    # 1. Initialization
    settings = load_settings()
    ui = Interface()
    
    # Show Splash Screen
    ui.show_splash(settings['app'].get('version', 'Unknown'))

    # 2. Initialize Core Components
    rotator = KeyRotator(key_pool_path='config/key_pool.yaml')
    
    # Inject Rotator into Engine
    engine = NexusEngine(
        rotator=rotator, 
        simulation_mode=settings['app'].get('simulation_mode', True)
    )

    # 3. Show Network Status
    ui.show_dashboard(rotator.pool)

    # 4. Main Interaction Loop
    while True:
        try:
            prompt = ui.get_input()
            
            # Exit conditions
            if prompt.lower() in ['exit', 'quit', '/q']:
                ui.print_stream("Disconnecting from secure node...", is_system=True)
                break
            
            if not prompt.strip():
                continue

            # Callback function to handle real-time output from Engine
            current_response_buffer = []
            
            def render_callback(chunk, is_system=False, is_error=False):
                if chunk is None: 
                    # End of stream
                    ui.console.print("\n") # New line after generation
                    return 
                
                if is_system or is_error:
                    ui.print_stream(chunk, is_system, is_error)
                else:
                    ui.print_stream(chunk)

            # Execute
            engine.execute_prompt(prompt, render_callback)

        except KeyboardInterrupt:
            ui.print_stream("\nSession terminated by user.", is_error=True)
            break
        except Exception as e:
            ui.print_stream(f"Unexpected Error: {e}", is_error=True)

if __name__ == "__main__":
    main()
