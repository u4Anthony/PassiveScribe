#!/usr/bin/env python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

input_path = './RevInput'
output_path = './RevOutput'

class NewEventHandler(FileSystemEventHandler):
    device_type = 'cpu'

    def __init__(self, callback, device_type):
        self.callback = callback
        self.device_type = device_type
        super().__init__()

    def on_created(self, event):
        self.callback(event.src_path, output_path, self.device_type, is_directory=event.is_directory)

class Checker():
    device_type = 'cpu'

    def __init__(self, device_type):
        self.device_type = device_type

    def watch(self, callback):
        event_handler = NewEventHandler(callback, self.device_type)
        observer = Observer()
        observer.schedule(event_handler, input_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()