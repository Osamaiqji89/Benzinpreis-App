class StatusLogger:
    """
    A centralized logging utility to update status across the application.
    Can be used in any class without direct reference to MainWindow.
    """
    _status_bar = None

    @classmethod
    def set_status_bar(cls, status_bar):
        """
        Set the status bar reference once during application initialization.
        
        :param status_bar: QStatusBar instance from MainWindow
        """
        cls._status_bar = status_bar

    @classmethod
    def log(cls, message, duration=5000):
        """
        Log a message to the status bar.
        
        :param message: Message to display
        :param duration: How long to show the message (milliseconds)
        """
        if cls._status_bar:
            cls._status_bar.showMessage(str(message), duration)
        else:
            # Fallback to print if status bar is not set
            print(f"[STATUS] {message}")

    @classmethod
    def error(cls, message, duration=5000):
        """
        Log an error message to the status bar.
        
        :param message: Error message to display
        :param duration: How long to show the message (milliseconds)
        """
        cls.log(f"Error: {message}", duration)

    @classmethod
    def success(cls, message, duration=3000):
        """
        Log a success message to the status bar.
        
        :param message: Success message to display
        :param duration: How long to show the message (milliseconds)
        """
        cls.log(f"Success: {message}", duration)
