import wave, struct, sys

def recover_lsb_watermark(watermarked_filepath):
    # Simply collect the LSB from each sample
    watermarked_audio = wave.open(watermarked_filepath, 'rb')

    (nchannels, sampwidth, framerate, nframes, comptype, compname) = watermarked_audio.getparams()
    frames = watermarked_audio.readframes (nframes * nchannels)
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)

    # determine how many watermark bytes we should look for
    watermark_bytes = 0
    for (sample,i) in zip(samples[0:32], range(0,32)):
        watermark_bytes = watermark_bytes + ( (sample & 1) * (2 ** i))

    print("Recovering %d bytes of watermark information from %s (%d samples)" % (watermark_bytes, watermarked_filepath, len(samples)))

    watermark_data = []

    for n in range(0, watermark_bytes):
        watermark_byte_samples = samples[32 + (n * 8) : 32+((n+1) * 8)]
        watermark_byte = 0
        for (sample, i) in zip(watermark_byte_samples, range(0,8)):
            watermark_byte = watermark_byte + ( (sample & 1) * (2**i) )
        watermark_data.append(watermark_byte)
    return watermark_data

def recover_embedded_file(encoded_signal, hidden_data_dest):
		wm = recover_lsb_watermark(encoded_signal)
		wm_str = watermark_to_string(wm)
		f = open(hidden_data_dest,"w")
		f.write(wm_str)

def watermark_to_string(list):
    return "".join([chr(x) for x in list])

if __name__ == "__main__":
		encoded_audio = "output/secret.wav"
		secret_output = "secrets.txt"
		recover_embedded_file(encoded_audio, secret_output)
