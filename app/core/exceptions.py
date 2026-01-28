from fastapi import HTTPException, status

class ChatbotException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class LeadNotFoundException(ChatbotException):
    def __init__(self, message: str = "Lead not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class ConversationNotFoundException(ChatbotException):
    def __init__(self, message: str = "Conversation not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class LeadRegistrationRequiredException(ChatbotException):
    def __init__(self, message: str = "Lead registration required"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)
