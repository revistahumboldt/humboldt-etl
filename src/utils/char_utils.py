
class CharUtils:

    @staticmethod
    def remove_invalid_chars(text: str) -> str:
        """Removes characters that cannot be encoded."""
        if text:
            return text.encode('utf-8', errors='ignore').decode('utf-8')
        return text
