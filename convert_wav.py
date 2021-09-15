import wave
import numpy as np

import librosa
import soundfile as sf


def save_wav_channel(fn, wav, channel):
    '''
    Take Wave_read object as an input and save one of its
    channels into a separate .wav file.
    '''
    # Read data
    nch = wav.getnchannels()
    depth = wav.getsampwidth()
    wav.setpos(0)
    sdata = wav.readframes(wav.getnframes())

    # Extract channel data (24-bit data not supported)
    typ = {1: np.uint8, 2: np.uint16, 4: np.uint32}.get(depth)
    if not typ:
        raise ValueError("sample width {} not supported".format(depth))
    if channel >= nch:
        raise ValueError("cannot extract channel {} out of {}".format(channel + 1, nch))
    print("Extracting channel {} out of {} channels, {}-bit depth".format(channel + 1, nch, depth * 8))
    data = np.fromstring(sdata, dtype=typ)
    ch_data = data[channel::nch]

    # Save channel to a separate file
    outwav = wave.open(fn, 'w')
    outwav.setparams(wav.getparams())
    outwav.setnchannels(1)
    outwav.writeframes(ch_data.tostring())
    outwav.close()


def convert_frame_rate(in_file, out_file, target_sr=16000):
    y, sr = librosa.load(in_file, sr=target_sr)
    print(sr)
    sf.write(out_file, y, target_sr, subtype='PCM_16')


if __name__ == "__main__":
    for i in range(1, 51):
        wav_file = wave.open("test_cases/{}.wav".format(i))
        save_wav_channel("test_cases/channel0/{}.wav".format(i), wav_file, 0)
        save_wav_channel("test_cases/channel1/{}.wav".format(i), wav_file, 1)

        # convert to 16000 frame rate
        convert_frame_rate("test_cases/channel0/{}.wav".format(i), "test_cases/channel0_16k/{}.wav".format(i))
        convert_frame_rate("test_cases/channel1/{}.wav".format(i), "test_cases/channel1_16k/{}.wav".format(i))
