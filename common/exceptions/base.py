from rest_framework import status


class ApplicationException(Exception):
    """
    Custom exception to be used for application-specific errors.
    """
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
