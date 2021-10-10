#!/usr/bin/env python

#- * -coding: utf - 8 - * -#Import the json library
import requests
import json

class ViettelSTTClient(object):

    def __init__(self):
        self.url = "https://viettelgroup.ai/voice/api/asr/v1/rest/decode_file"

    def decode(self, audio_bytes: bytes):
        headers = {
            "token": "anonymous",
            #"sample_rate": 16000,
            #"format": "S16LE",
            #"num_of_channels": 1,
            #"asr_model": "model code"
        }
        files = {
            "file": audio_bytes
        }
        response = requests.post(self.url, files = files, headers = headers)
        res_dict = json.loads(response.text)
        print(res_dict)
        return res_dict[0]["result"]["hypotheses"][0]["transcript"]


# [{
#     "status": 0,
#     "msg": "STATUS_SUCCESS",
#     "segment": 0,
#     "result": {
#         "hypotheses": [{
#             "transcript": "một hai ba bốn năm sáu bảy",
#             "transcript_normed": "một hai ba bốn năm sáu bảy",
#             "confidence": 0.5,
#             "likelihood": 50
#         }],
#         "final": true
#     },
#     "segment_start": 0.42,
#     "segment_length": 3.87,
#     "total_length": 3.87
# }]
