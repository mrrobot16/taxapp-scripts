import json
import re

# TODO: Need to create a method that I pass a string and it should extract numbers inside and convert/return an array with those numbers number inside of such string 
# Example string:  """{'pdf_file_name': '17.txt', 'status': 400, 'error': BadRequestError('Error code: 400 - {\'error\': {\'message\': "This model\'s maximum context length is 128000 tokens. However, your messages resulted in 267105 tokens. Please reduce the length of the messages.", \'type\': \'invalid_request_error\', \'param\': \'messages\', \'code\': \'context_length_exceeded\'}}')}"""
# Only extract the numbers that are after 'message':... 
# ie: 'message\': "This model\'s maximum context length is 128000 tokens. However, your messages resulted in 267105 tokens. Please reduce the length of the messages."
# Example output: [128000, 267105]

class APIError(Exception):
    def __init__(self, message, error_type=None, code=None, param=None, additional_info=None):
        super().__init__(message)
        self.type = error_type
        self.code = code
        self.param = param
        self.additional_info = additional_info

    @staticmethod
    def extract_numbers_after_message(input_string):
        match = re.search(r"'message':.*", input_string)
        if match:
            message_part = match.group()
            numbers = re.findall(r'\d+', message_part)
            return [int(num) for num in numbers]
        else:
            return []  # Return an empty list if 'message': is not found

    @staticmethod
    def extract_code_value(input_string):
        match = re.search(r"'code':\s*'(\w+)'", input_string)
        if match:
            return match.group(1)
        else:
            return None  # Return None if 'code': is not found

    @staticmethod
    def parse_api_error(error_message):
        try:
            json_str = re.search(r'\{.*\}', error_message).group()
            error_data = json.loads(json_str)
            message = error_data.get('error', {}).get('message', '')
            error_type = error_data.get('error', {}).get('type', '')
            code = error_data.get('error', {}).get('code', '')
            param = error_data.get('error', {}).get('param', '')
            additional_info = {k: v for k, v in error_data.items() if k not in ['error']}
            return APIError(message, error_type, code, param, additional_info)
        except Exception as e:
            print('error', e)
            return None


error_message_rate_limit_exceeded = """{'status': 400, 'message': "chat_completion error: Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4-1106-preview in organization org-TEIBD5u31eD65gkVjqjTc6LN on tokens_usage_based per min: Limit 300000, Used 257348, Requested 79228. Please try again in 7.315s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens_usage_based', 'param': None, 'code': 'rate_limit_exceeded'}}", 'error': RateLimitError("Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4-1106-preview in organization org-TEIBD5u31eD65gkVjqjTc6LN on tokens_usage_based per min: Limit 300000, Used 257348, Requested 79228. Please try again in 7.315s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'type': 'tokens_usage_based', 'param': None, 'code': 'rate_limit_exceeded'}}")}"""
error_message_context_length_exceeded = """{'pdf_file_name': '17.txt', 'status': 400, 'error': BadRequestError('Error code: 400 - {\'error\': {\'message\': "This model\'s maximum context length is 128000 tokens. However, your messages resulted in 267105 tokens. Please reduce the length of the messages.", \'type\': \'invalid_request_error\', \'param\': \'messages\', \'code\': \'context_length_exceeded\'}}')}"""

parsed_error = parse_api_error(error_message)
if parsed_error:
    print(f"Message: {parsed_error.message}")
    print(f"Type: {parsed_error.type}")
    print(f"Code: {parsed_error.code}")
    print(f"Param: {parsed_error.param}")
    print(f"Additional Info: {parsed_error.additional_info}")
else:
    print("Error parsing the API error message.")


parsed_error_rate_limit = APIError.parse_api_error(error_message_rate_limit_exceeded)
if parsed_error_rate_limit:
    print(f"Message: {parsed_error_rate_limit.message}")
    print(f"Type: {parsed_error_rate_limit.type}")
    print(f"Code: {parsed_error_rate_limit.code}")
    print(f"Param: {parsed_error_rate_limit.param}")
    print(f"Additional Info: {parsed_error_rate_limit.additional_info}")

# Extracting numbers after 'message':
numbers_rate_limit = APIError.extract_numbers_after_message(error_message_rate_limit_exceeded)
print(f"Numbers after 'message' in rate limit error: {numbers_rate_limit}")

# Extracting the code value:
code_value_rate_limit = APIError.extract_code_value(error_message_rate_limit_exceeded)
print(f"Code value in rate limit error: {code_value_rate_limit}")