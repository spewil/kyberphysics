import numpy as np
import scipy.signal
import scipy.ndimage

from utils import utils


def load_bin_file(path):
    return np.fromfile(path, dtype=np.int32)


def preprocess_emg(recording,
                   nch=32,
                   start=200,
                   end=-1,
                   lowcutoff=5,
                   highcutoff=60,
                   mean=None):
    # highpass, rectify, lowpass, mean subtract per channel
    data_subset = recording[:nch, :]
    for channel, t in enumerate(data_subset):
        data_subset[channel, :] = lowpass(rectify(
            highpass(data_subset[channel, :], cutoff=highcutoff)),
                                          cutoff=lowcutoff)
    if mean is None:
        out = data_subset - data_subset[:, start - 1:end].mean(axis=1).reshape(
            -1, 1)
    else:
        out = data_subset - mean
    return out[:, start - 1:end]


def rectify(a):
    return np.abs(a)


def highpass(sig, cutoff=50):
    b, a = scipy.signal.butter(2, cutoff, 'highpass', analog=False, fs=2000)
    return scipy.signal.filtfilt(b, a, sig, axis=-1)


def lowpass(sig, cutoff=500):
    b, a = scipy.signal.butter(2, cutoff, 'lowpass', analog=False, fs=2000)
    return scipy.signal.filtfilt(b, a, sig, axis=-1)


def notch(sig, freq=50):
    """
        Not really sure how to tune this effectively... 
    """
    b, a = scipy.signal.iirnotch(freq, 30, fs=2000)
    return scipy.signal.filtfilt(b, a, sig, axis=-1)


def moving_average(a, window_length=100):
    """
        boxcar window average
    """
    return scipy.ndimage.convolve1d(
        a, np.ones((window_length)), axis=1, mode='nearest') / window_length


def blur(a, sigma=50):
    """
        gaussian convolution
    """
    return scipy.ndimage.gaussian_filter1d(a,
                                           sigma=sigma,
                                           axis=1,
                                           mode='nearest')


def demean(a):
    assert a.shape[0] < a.shape[1]
    return a - np.mean(a, axis=1).reshape(-1, 1)


def preprocess(data, sigma=40):
    data_mv = data * 0.0002861
    data_mv = demean(data_mv)
    output = rectify(data_mv)
    output = blur(output, sigma)
    return output


def get_dropped_samples(counter):
    if len(counter.shape) > 1:
        counter = counter[0]
    drops = (counter[1:] - counter[:-1]) - 1
    drops[np.where(drops == -(2**16))] = 0
    for idx in np.where(drops != 0):
        print(f"Dropped {drops[idx]} samples at {idx}")
    return drops


def fill_time_array(dataset):
    dataset['time'] = np.arange(0,
                                len(dataset.time) / dataset.sampling_rate,
                                1 / dataset.sampling_rate)


if __name__ == "__main__":
    print("analysis!")
    print(dir(utils))