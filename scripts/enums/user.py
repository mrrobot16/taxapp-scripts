from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'
    SYSTEM = 'system'
    ASSISTANT = 'assistant'

class UserAuthType(Enum): 
    EMAIL_PASSWORD = 'email-password'
    LOCAL = 'local'