import os
import glob

from tritonclient.grpc import service_pb2_grpc
from tritonclient.grpc import service_pb2
import grpc
import time
import librosa
import soundfile as sf
import tqdm
import numpy as np
import base64
import tempfile

SENDING_RATE = 0.5
TARGET_SR = 16000


def generate_message(audio, sample_rate):
    audio = audio
    len_audio = audio.shape[0]
    batch_size = round(sample_rate * SENDING_RATE)
    num_batch = len_audio // batch_size

    for i in range(int(num_batch)):
        f = i * batch_size
        t = min((i + 1) * batch_size, len_audio)
        b_audio = audio[f:t]

        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav")
        sf.write(tmp_file.name, b_audio, sample_rate)
        bytes_obj = open(tmp_file.name, 'rb').read()
        tmp_file.close()

        request = service_pb2.ModelInferRequest()
        request.raw_input_contents.append(bytes_obj)

        yield request


def start_asr(fn, stub):
    start = time.time()
    audio, sr = librosa.load(fn, TARGET_SR)
    au, sr = sf.read(fn)
    au = librosa.resample(au, sr, TARGET_SR).astype(np.float32)
    responses = stub.ModelStreamInfer(
        generate_message(audio.astype(np.float32), TARGET_SR))
    for response in responses:
        result = response.infer_response.raw_output_contents[0].decode('utf8')
        is_stop = response.infer_response.raw_output_contents[1]
    return result


def streaming_test_e2e(stub):
    folder = '../ASR/data/common-voice-test/'
    files = glob(os.path.join(folder, '*/*.wav'))
    files = [os.path.abspath(fn) for fn in files]
    resutls = {}
    for fn in tqdm(files):
        resutls[fn] = start_asr(fn, stub)
    return resutls


class STTClient(object):

    def __init__(self):
        with open("./stt/server.crt", "rb") as f:
            trusted_certs = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel("medical-asr-service-grpc-int.draid.ai:8001", credentials)
        self.stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)
        print("Done init grpc connection to stt server!")

    def inferBase64(self, base64_audio):
        file_name = "./stt/example_data/tmp.wav"
        with open(file_name, "wb") as f:
            f.write(base64.b64decode(base64_audio))
            # text = start_asr(file_name, self.stub)

        # return text
        return "fake_text"


def test_case():
    print("Init server...")
    file_name = "example_data/tmp.wav"
    with open("./server.crt", "rb") as f:
        trusted_certs = f.read()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel("medical-asr-service-grpc-int.draid.ai:8001", credentials)
    stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)
    print("Done init server!")

    start_asr(file_name, stub)


if __name__ == "__main__":
    test_case()
    print("")
