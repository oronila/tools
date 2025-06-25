#!/usr/bin/env python3
"""
Anti-AFK Tool
Monitors mouse movement and prevents computer from going to sleep by moving mouse
when user has been inactive for more than 3 minutes.
"""

import time
import threading
import random
import pyautogui
from datetime import datetime, timedelta


class AntiAFKTool:
    def __init__(self, afk_timeout_minutes=3):
        self.afk_timeout = timedelta(minutes=afk_timeout_minutes)
        self.last_activity = datetime.now()
        self.running = True
        self.monitor_thread = None
        self.last_mouse_pos = pyautogui.position()
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        pyautogui.PAUSE = 0.1  # Small pause between actions
        
        print(f"Anti-AFK Tool initialized with {afk_timeout_minutes} minute timeout")
        print("Press Ctrl+C to stop the tool")
        print("Move mouse to top-left corner to emergency stop")
    
    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = datetime.now()
    
    def check_mouse_movement(self):
        """Check if mouse has moved since last check"""
        try:
            current_mouse_pos = pyautogui.position()
            if current_mouse_pos != self.last_mouse_pos:
                self.last_mouse_pos = current_mouse_pos
                self.update_activity()
                return True
        except Exception as e:
            print(f"Error checking mouse position: {e}")
        
        return False
    
    def move_mouse_slightly(self):
        """Move mouse by a small random amount to simulate activity"""
        try:
            current_pos = pyautogui.position()
            
            # Move mouse by a small random amount (1-5 pixels)
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            
            new_x = max(0, min(current_pos[0] + dx, pyautogui.size()[0] - 1))
            new_y = max(0, min(current_pos[1] + dy, pyautogui.size()[1] - 1))
            
            # Move mouse slightly
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            
            # Move it back to original position
            time.sleep(0.1)
            pyautogui.moveTo(current_pos[0], current_pos[1], duration=0.1)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Mouse moved to prevent AFK")
            
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def monitor_activity(self):
        """Monitor mouse movement and move mouse when AFK detected"""
        print("Starting mouse movement monitoring...")
        print(f"Checking every 3 seconds, will move mouse after {self.afk_timeout.total_seconds():.0f} seconds of inactivity")
        
        while self.running:
            try:
                # Check for mouse movement
                mouse_moved = self.check_mouse_movement()
                
                # Calculate time since last activity
                time_since_activity = datetime.now() - self.last_activity
                
                if time_since_activity >= self.afk_timeout:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] AFK detected after {time_since_activity.total_seconds():.0f} seconds - moving mouse")
                    self.move_mouse_slightly()
                    # Reset activity timer to prevent constant mouse movement
                    self.update_activity()
                elif mouse_moved:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Mouse movement detected - resetting timer")
                
                # Check every 3 seconds
                time.sleep(3)
                
            except pyautogui.FailSafeException:
                print("Emergency stop activated - mouse moved to corner")
                self.stop()
                break
            except Exception as e:
                print(f"Error in monitoring: {e}")
                time.sleep(3)
    
    def start(self):
        """Start the anti-AFK tool"""
        try:
            print("Starting Anti-AFK Tool...")
            print(f"Screen size: {pyautogui.size()}")
            print(f"Current mouse position: {pyautogui.position()}")
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_activity, daemon=True)
            self.monitor_thread.start()
            
            print("Anti-AFK Tool is now running...")
            print("The tool will move your mouse if no movement detected for 3+ minutes")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nShutting down Anti-AFK Tool...")
            self.stop()
        except Exception as e:
            print(f"Error starting tool: {e}")
            self.stop()
    
    def stop(self):
        """Stop the anti-AFK tool"""
        self.running = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        print("Anti-AFK Tool stopped")


def main():
    """Main function"""
    print("=" * 50)
    print("        Anti-AFK Tool (PyAutoGUI)")
    print("=" * 50)
    print("This tool prevents your computer from going to sleep")
    print("by moving the mouse when no movement detected for 3+ minutes")
    print("=" * 50)
    
    try:
        tool = AntiAFKTool(afk_timeout_minutes=3)
        tool.start()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main() 