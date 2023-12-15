from enum import Enum

class OpenAIModel(Enum):
    GPT_4 = 'gpt-4-0613'
    GPT_4_32K = 'gpt-4-32k-0613'
    GPT_4_1106_PRE = 'gpt-4-1106-preview'
    GPT_3_5_TURBO = 'gpt-3.5-turbo-0613'
    GPT_3_5_TURBO_16K = 'gpt-3.5-turbo-16k-0613'

class OpenAIObjectType(Enum):
    CHAT_COMPLETION = 'chat.completion'
    TEXT_COMPLETION = 'text_completion'
    TEXT_MODERATION = 'text-moderation-005'