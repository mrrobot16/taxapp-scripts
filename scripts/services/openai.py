import openai

from constants.openai import (
    OPENAI_ENGINE, 
    OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, 
    OPENAI_ASSISTANT_PROMPT, OPENAI_SYSTEM_PROMPT, OPENAI_USER_PROMPT, 
    OPENAI_API_KEY_DEV
)


class OpenAIService:

    def __init__(self, keys = OPENAI_API_KEY_DEV):
        openai.api_key = keys

    def chat_completion(
        self,
        prompt, 
        engine = OPENAI_ENGINE.value,
        system_prompt = OPENAI_SYSTEM_PROMPT, 
        assistant_prompt = OPENAI_ASSISTANT_PROMPT,
        temperature = OPENAI_TEMPERATURE,  
        max_tokens = OPENAI_MAX_TOKENS,
    ):
    
        try:
            # NOTE: prompt.encode().decode() is used to remove non-ASCII characters from the prompt.
            user_prompt = {
                "role": "user",
                "content": prompt.encode(encoding = 'ASCII', errors = 'ignore').decode() + ". "
            }
            response = openai.chat.completions.create(
                model = engine,
                messages = [
                    system_prompt,
                    assistant_prompt,
                    user_prompt,
                ],
                temperature = temperature,
                max_tokens = max_tokens
            )
            # message = response.choices[0].message
            # print("\n")
            # print('response', response)
            message = response.choices[0].message
            # print("\n")
            # print('message', message)
            content = message.content
            # print("\n")
            # print('content:', content)
            return {
                'status': 200,
                'message': message.content,

            }
            # print('content', content)
            # openai_api_response_model = ChatCompletionResponseModel(message = message.model_dump())
            # openai_response_model = OpenAIChatCompletionObjectResponseModel(**response.model_dump())
            # return {
            #     "api": openai_api_response_model.model_dump(),
            #     "open_ai_chat_completion_api": openai_response_model.model_dump()
            # }
        except Exception as error:
            return {
                'status': 400,
                'message': f"chat_completion error: {error}",
                'error': error
            }
 
def openai_service():
    return OpenAIService()