#!/usr/bin/env python3
"""
Anti-AFK Tool
Monitors user activity and prevents computer from going to sleep by moving mouse
when user has been inactive for more than 3 minutes.
"""

import time
import threading
import random
from datetime import datetime, timedelta
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


class AntiAFKTool:
    def __init__(self, afk_timeout_minutes=3):
        self.afk_timeout = timedelta(minutes=afk_timeout_minutes)
        self.last_activity = datetime.now()
        self.mouse_controller = mouse.Controller()
        self.running = True
        self.mouse_listener = None
        self.keyboard_listener = None
        self.monitor_thread = None
        
        print(f"Anti-AFK Tool initialized with {afk_timeout_minutes} minute timeout")
        print("Press Ctrl+C to stop the tool")
    
    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = datetime.now()
    
    def on_mouse_move(self, x, y):
        """Callback for mouse movement"""
        self.update_activity()
    
    def on_mouse_click(self, x, y, button, pressed):
        """Callback for mouse clicks"""
        if pressed:
            self.update_activity()
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Callback for mouse scrolling"""
        self.update_activity()
    
    def on_key_press(self, key):
        """Callback for key presses"""
        self.update_activity()
    
    def move_mouse_slightly(self):
        """Move mouse by a small random amount to simulate activity"""
        current_pos = self.mouse_controller.position
        
        # Move mouse by a small random amount (1-3 pixels)
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        
        new_x = current_pos[0] + dx
        new_y = current_pos[1] + dy
        
        self.mouse_controller.position = (new_x, new_y)
        
        # Move it back to original position after a short delay
        time.sleep(0.1)
        self.mouse_controller.position = current_pos
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mouse moved to prevent AFK")
    
    def monitor_activity(self):
        """Monitor for AFK status and move mouse when needed"""
        while self.running:
            time_since_activity = datetime.now() - self.last_activity
            
            if time_since_activity >= self.afk_timeout:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] AFK detected - moving mouse")
                self.move_mouse_slightly()
                # Reset activity timer to prevent constant mouse movement
                self.update_activity()
            
            # Check every 30 seconds
            time.sleep(30)
    
    def start_listeners(self):
        """Start mouse and keyboard listeners"""
        # Start mouse listener
        self.mouse_listener = MouseListener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        # Start keyboard listener
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_key_press
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        print("Activity listeners started")
    
    def stop_listeners(self):
        """Stop mouse and keyboard listeners"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        print("Activity listeners stopped")
    
    def start(self):
        """Start the anti-AFK tool"""
        try:
            print("Starting Anti-AFK Tool...")
            
            # Start activity listeners
            self.start_listeners()
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_activity, daemon=True)
            self.monitor_thread.start()
            
            print("Anti-AFK Tool is now running...")
            print("The tool will move your mouse if you're inactive for more than 3 minutes")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nShutting down Anti-AFK Tool...")
            self.stop()
    
    def stop(self):
        """Stop the anti-AFK tool"""
        self.running = False
        self.stop_listeners()
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        print("Anti-AFK Tool stopped")


def main():
    """Main function"""
    print("=" * 50)
    print("        Anti-AFK Tool")
    print("=" * 50)
    print("This tool prevents your computer from going to sleep")
    print("by moving the mouse when you're inactive for 3+ minutes")
    print("=" * 50)
    
    tool = AntiAFKTool(afk_timeout_minutes=3)
    tool.start()


if __name__ == "__main__":
    main() 