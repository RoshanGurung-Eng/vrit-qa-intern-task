class AutomationError(Exception):
    """Base exception for automation failures."""
    pass

class ElementNotFoundError(AutomationError):
    """Raised when a required element is not found."""
    pass

class OTPExtractionError(AutomationError):
    """Raised when OTP cannot be extracted."""
    pass

class FormSubmissionError(AutomationError):
    """Raised when form submission fails."""
    pass