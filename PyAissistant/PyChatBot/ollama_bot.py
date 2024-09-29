from ollama_api import OllamaClient

from .chat_api import ChatBot
from .chat_bot_util import *


class OllamaBot(ChatBot):

    def __init__(self, post_words=print_words):
        super().__init__(post_words)
        self.stream = True
        self.client = OllamaClient()

    def _generate_response(self, user_input: str):
        lines = {}
        # response = self.client.request_completion(model="llama3.1", stream=True, prompt=message)
        chain = self.message_chain()
        response = self.client.request_chat_completion(model="llama3.1", messages=chain, stream=self.stream)
        if self.stream:
            response.raise_for_status()
            msg_stack = ""
            lineIndex = 0

            # {"model":"llama3.1",
            # "created_at":"2024-07-25T06:35:52.9797747Z",
            # "response":"","done":true,
            # "done_reason":"stop",
            # "context":[128009,128006,882,128007,271,35563,13180,374,6437,128009,128006,78191,128007,271,32,11670,1715,2268,791,2944,279,13180,8111,6437,374,4245,311,264,10824,315,12624,16565,11,11951,1473,16,13,3146,14235,72916,96618,3277,40120,29933,9420,596,16975,11,433,35006,13987,35715,315,45612,1778,439,47503,320,45,17,8,323,24463,320,46,17,570,4314,35715,45577,279,3177,304,682,18445,627,18,13,3146,54,35961,82,323,8146,96618,34496,93959,315,3177,527,38067,311,29865,12628,13,8868,3177,706,264,24210,46406,1109,2579,3177,11,3339,433,810,6847,38067,555,279,2678,35715,304,279,16975,382,8586,596,279,3094,14656,30308,16540,1473,334,8468,220,16,25,8219,4238,29933,279,16975,57277,791,7160,73880,4251,3177,11,902,17610,315,682,279,8146,315,279,9621,20326,320,1171,11,19087,11,14071,11,6307,11,6437,11,1280,7992,11,323,80836,570,3277,420,40120,25501,9420,596,16975,11,433,35006,13987,35715,315,45612,382,334,8468,220,17,25,8828,72916,13980,57277,9673,6962,35715,45577,279,3177,304,682,18445,13,4452,11,439,9932,6931,11,24210,93959,1093,6437,3177,527,38067,810,1109,5129,93959,1093,2579,3177,382,334,8468,220,18,25,8868,3177,83978,279,13180,57277,2170,264,1121,315,420,72916,1920,11,279,6437,3177,374,4332,6957,279,16975,323,25501,1057,6548,505,682,18445,13,1115,374,3249,584,45493,279,13180,439,6437,382,1271,20461,420,25885,11,2980,1473,9,3146,16440,82,96618,1952,264,74649,1938,11,279,7160,596,45220,617,311,5944,1555,810,16975,311,5662,701,6548,13,1666,264,1121,11,1524,810,6437,3177,374,38067,11,3339,279,13180,5101,459,1524,19662,28601,315,6437,627,9,3146,26777,25793,96618,763,5789,449,1579,5990,315,3805,25793,11,279,13987,19252,304,279,16975,649,45577,3177,304,5370,18445,11,18189,279,21261,315,6437,3177,323,7231,279,13180,264,305,13933,477,18004,819,11341,382,334,8991,12519,278,11311,57277,1271,3493,264,810,47616,16540,11,584,649,1005,13558,64069,596,2383,11,902,16964,279,72916,315,3177,555,2678,35715,1473,40,12264,251,220,16,14,34586,61,19,271,2940,358,374,279,38067,21261,11,49438,374,279,46406,315,3177,11,323,279,21801,2786,6926,374,11075,555,279,6012,315,279,45577,261,320,258,420,1162,11,3805,35715,3677,2028,24524,5039,430,24210,93959,320,4908,6437,3177,8,527,38067,810,1109,5129,93959,320,4908,2579,3177,705,902,15100,3249,584,1518,264,47904,6437,13180,382,8142,358,3077,6818,311,3493,264,16195,16540,11,4587,5296,430,279,37072,96354,374,44899,323,10825,369,2536,18882,15916,13,1442,499,4265,1093,311,82845,19662,1139,279,22027,315,3177,72916,11,1070,596,11510,315,17649,389,279,8712,0],
            # "total_duration":6655006100,"load_duration":16484100,
            # "prompt_eval_count":15,
            # "prompt_eval_duration":230090000,
            # "eval_count":513,
            # "eval_duration":6407754000}

            for chunk in response.iter_content(chunk_size=1024):
                msg_stack += chunk.decode('utf-8')  # Decode bytes to string
                lines = msg_stack.splitlines()
                if len(lines) > lineIndex + 1:
                    line = lines[lineIndex]
                    lineIndex += 1
                    self._write_out(try_get_allama_words(line))
            while len(lines) > lineIndex:
                line = lines[lineIndex]
                self._write_out(try_get_allama_words(line))
                lineIndex += 1
            return msg_stack, generate_uuid(32), None
        else:
            # json;
            item = response.json()
            # model = item.get("model")
            # created_at = item.get("created_at")
            message = item.get("message")
            # done_reason = item.get("done_reason")
            # done = item.get("done")
            # total_duration = item.get("total_duration")
            # load_duration = item.get("load_duration")
            # prompt_eval_count = item.get("prompt_eval_count")
            # prompt_eval_duration = item.get("prompt_eval_duration")
            # eval_count = item.get("eval_count")
            # eval_duration = item.get("eval_duration")
            msg_content = message.get("content")
            # msg_role = message.get("role")
            self._write_out(msg_content)
            return msg_content, generate_uuid(32), None
