import pyaudio
import numpy as np
import wave

CHUNK = 8192 #32768

# use a Blackman window
window = np.blackman(CHUNK)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000

p = pyaudio.PyAudio()
myStream = None
try:
    myStream = p.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = CHUNK)
except:
    pass

def analyseStream():
    if myStream == None: return np.array([]) if CHANNELS == 1 else np.array([[],[]])
    
    while myStream.get_read_available() == 0:
        pass
    
    available = myStream.get_read_available()
    chunk_count = int(available / CHUNK)
    data = ""
    if chunk_count > 1:
        for i in xrange(0, chunk_count):
            try:
                tmp = myStream.read(CHUNK)
            except IOError as inst:
                print "Caught an IOError on stream read.", inst
        data += tmp
    elif chunk_count == 1:
        data = myStream.read(CHUNK)

    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(CHUNK*chunk_count), data))

    # Take the fft and square each value
    fftData = abs(np.fft.fft(indata * window))
    fftData = fftData * 1.0 / len(fftData)

    epsilon = 1e-30
    db_spectrogram = 20*np.log10(fftData + epsilon)
    return db_spectrogram


if __name__ == "__main__":
    for i in xrange(2):
        print len(analyseStream())
