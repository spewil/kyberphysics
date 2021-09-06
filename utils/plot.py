import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
import numpy as np
from math import radians
import seaborn as sns


def save_figure(fig, name, folder="."):
    # if folder doesn't exist, make it
    if folder != ".":
        Path(folder).mkdir(exist_ok=True, parents=True)
        savepath = Path(folder) / Path(name + ".pdf")
    else:
        savepath = Path(name + "pdf")
    fig.savefig(savepath,
                pad_inches=0.1,
                bbox_inches="tight",
                dpi=300,
                format="pdf",
                transparent=False)


def get_cmap(n_levels, cmap_name="viridis"):
    return plt.cm.get_cmap(cmap_name, n_levels)


def make_color_vector(cmap_name, n_levels):
    return [plt.cm.get_cmap(cmap_name, n_levels)(n) for n in range(n_levels)]


def plot_single_trajectory(trajectory, title=None):
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    axes[0].plot(trajectory[0])
    axes[1].plot(trajectory[1])
    axes[0].set_xlabel("Time")
    axes[1].set_xlabel("Time")
    axes[0].set_ylabel("Theta")
    axes[1].set_ylabel("Radius")
    if not title is None:
        axes[0].set_title(title)


def make_polar_plot():
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection="polar")
    ax.set_yticks([])
    #     ax.set_xlim([np.pi+np.pi/7,-np.pi/7])
    ax.set_ylim([0, 420])
    ax.set_xticks([0, radians(10), radians(170), np.pi])
    ax.set_xticklabels(
        ["$0^{\circ}$", "$10^{\circ}$", "$170^{\circ}$", "$180^{\circ}$"],
        FontSize=18)
    ax.spines['polar'].set_visible(False)
    return fig, ax


def make_polar_plot():
    fig = plt.figure(figsize=(18, 18))
    ax = fig.add_subplot(projection="polar")
    ax.set_yticks([])
    #     ax.set_xlim([np.pi+np.pi/7,-np.pi/7])
    ax.set_ylim([0, 420])
    ax.set_xticks([0, np.pi])
    ax.set_xticklabels(["$0^{\circ}$", "$180^{\circ}$"], FontSize=20)
    ax.spines['polar'].set_visible(False)
    return fig, ax


def make_ridgeplot(curve_matrix,
                   title=None,
                   nbins=20,
                   xlims=[100, 400],
                   xlabel=None,
                   ax=None,
                   cbax=None,
                   cmap=None,
                   fig=None):
    n_timepoints = curve_matrix.shape[1]
    if fig == None:
        fig = plt.figure(figsize=(8, 6))
    else:
        fig = fig
    if ax == None:
        spec = matplotlib.gridspec.GridSpec(ncols=2,
                                            nrows=1,
                                            width_ratios=[20, 1])
        ax = fig.add_subplot(spec[0])
        cbax = fig.add_subplot(spec[1])
        cbax.set_ylabel('time')
        cmap = matplotlib.cm.get_cmap('cividis')
        # norm = matplotlib.colors.Normalize(vmin=1, vmax=n_timepoints)

    else:
        ax = ax
        cbax = cbax
        cmap = cmap

    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlim(xlims)

    val_offsets = [i * 0.005 for i in range(n_timepoints)
                   ]  # how vertically spaced lines are
    time_offsets = [0 for i in range(n_timepoints)
                    ]  # how spaced distros are in time axis

    for i in range(n_timepoints):
        vals, bins = np.histogram(curve_matrix[:, i], density=True, bins=nbins)
        midpoints = [(b + bins[bi + 1]) / 2 for bi, b in enumerate(bins[:-1])]
        ax.plot([m + time_offsets[i] for m in midpoints],
                [v + val_offsets[i] for v in vals],
                color=cmap(i / n_timepoints),
                alpha=0.7,
                zorder=n_timepoints - i)

    return fig, ax


def make_distro_ridgeplot(x, curve_matrix, title=None):
    n_timepoints = curve_matrix.shape[1]
    # n_trials = curve_matrix.shape[0]
    fig = plt.figure(figsize=(8, 6))
    spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[20, 1])
    ax = fig.add_subplot(spec[0])
    cbax = fig.add_subplot(spec[1])
    cmap = matplotlib.cm.get_cmap('cividis')
    # norm = matplotlib.colors.Normalize(vmin=1, vmax=n_timepoints)
    # cb = matplotlib.colorbar.ColorbarBase(cbax,
    #                                       cmap=cmap,
    #                                       norm=norm,
    #                                       orientation='vertical')
    cbax.set_ylabel('time')
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel("radius")
    if title:
        ax.set_title(title)

    val_offsets = [i * 0.0005 for i in range(n_timepoints)
                   ]  # how vertically spaced lines are
    time_offsets = [0 for i in range(n_timepoints)
                    ]  # how spaced distros are in time axis

    for i in range(n_timepoints):
        # range of the distribution vs. distribution values
        # matrix should be distribution, num_distributions
        ax.plot([m + time_offsets[i] for m in x],
                [v + val_offsets[i] for v in curve_matrix[:, i]],
                color=cmap(i / n_timepoints),
                alpha=0.7,
                zorder=n_timepoints - i)
    return fig, ax


def plot_biolectric(data,
                    idxs_to_plot=None,
                    offset=1,
                    freq=2000,
                    figsize=(15, 10),
                    title=None):
    fig, ax = plt.subplots(figsize=figsize)
    if idxs_to_plot is None:
        idxs_to_plot = list(range(data.shape[0]))
    t = np.linspace(0, data.shape[1] / freq, data.shape[1])
    for i, idx in enumerate(idxs_to_plot):
        ax.plot(t, data[idx] + (i + 1) * offset)
    ax.set_yticks([(i + 1) * offset for i in range(len(idxs_to_plot))])
    ax.set_yticklabels([str(idx + 1) for idx in idxs_to_plot], FontSize=12)
    ax.set_ylabel("Channel")
    ax.set_xlabel("Time [s]")
    if title is not None:
        ax.set_title(title)
    return fig


def plot_features_bar(feature_vecs, title=None):
    fig = plt.figure()
    n_features = feature_vecs.shape[0]
    cm = get_cmap(n_features, 'viridis')
    axs = fig.subplots(n_features, 1, sharex=True)
    fig.subplots_adjust(hspace=0.5)
    for i, ax in zip(range(n_features), axs):
        ax.bar(range(len(feature_vecs[i].T)), feature_vecs[i].T, color=cm(i))
        ax.set_title(f"Component {i+1}", FontSize=12)
    if title is not None:
        fig.suptitle(title)
    return fig


## this is the layout of the BACK of the gridarray
def grid_layout(data, grid_type='8x8'):
    """
        transforms data into electrode layout
        data should be in [feature, sample] format
    """
    if len(data.shape) != 2:
        raise ValueError("data must be 2D")
    if grid_type == '8x8':
        pin_layout = np.array([[8, 16, 24, 32, 40, 48, 56, 64],
                               [7, 15, 23, 31, 39, 47, 55, 63],
                               [6, 14, 22, 30, 38, 46, 54, 62],
                               [5, 13, 21, 29, 37, 45, 53, 61],
                               [4, 12, 20, 28, 36, 44, 52, 60],
                               [3, 11, 19, 27, 35, 43, 51, 59],
                               [2, 10, 18, 26, 34, 42, 50, 58],
                               [1, 9, 17, 25, 33, 41, 49, 57]])
        pin_layout = pin_layout - 1
    elif grid_type == "band32":
        pin_layout = np.arange(32).reshape(4, -1)
    output = np.zeros(
        (pin_layout.shape[0], pin_layout.shape[1], data.shape[1]))
    for i, row in enumerate(pin_layout):
        for j, og_idx in enumerate(row):
            output[i, j, :] = data[og_idx, :]
    return output


def plot_biolectric_with_fft(data, idxs_to_plot):
    fig = plt.figure()
    num_plots = len(idxs_to_plot) * 2
    for i, idx in enumerate(idxs_to_plot):
        ax = fig.add_subplot(num_plots, 1, 2 * i + 1)
        ax.plot(data[idx])
        # Number of samplepoints
        N = 2000
        # sample spacing
        T = 1.0 / 2000.0
        x = np.linspace(0.0, N * T, N)
        yf = scipy.fftpack.fft(data[idx])
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
        ax_fft = fig.add_subplot(num_plots, 1, 2 * i + 2)
        ax_fft.plot(xf[:100], 2.0 / N * np.abs(yf[:N // 2][:100]))
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1, hspace=0.3)
    return fig


def plot_counter(counter):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if len(counter.shape) > 1:
        counter = counter[0]
    ax.plot(counter)
    # this should be 0 or the number of dropped
    # samples at the previous timepoint.
    drops = (counter[1:] - counter[:-1]) - 1
    drops[np.where(drops == -(2**16))] = 0
    ax.plot(drops)
    fig.suptitle("Device Sample Counter")
    return fig, ax


def plot_psd(data, freq=2000, legend=False, fig=None):
    dim = len(data.shape)
    if fig == None:
        fig, ax = plt.subplots(1, 1)

    if dim == 2:
        for i, channel in enumerate(data):
            ax.psd(channel,
                   Fs=freq,
                   detrend='linear',
                   label="Channel " + str(i))
            if legend:
                plt.legend()
    elif dim == 1:
        plt.figure()
        p = ax.psd(data, Fs=freq, detrend='linear', label='PSD')
    else:
        raise ValueError("data array must be 1D or 2D")
    # line = mlines.Line2D([50, 50], [-100, -50])
    # line.set_color('red')
    # line.set_linestyle('--')
    # ax.add_line(line)


def plot_events(events,
                events_per_row=12,
                sort=True,
                order=None,
                labels=None,
                title=None,
                save=False,
                filename=None):
    """Plot Motor units action potentials.

    Plot MUAPs.

    Parameters
    ----------
    events: list of np.ndarray
        list of events template. each template has a shape
        (n_electrodes x n_sample)
    events_per_row: int
        number of events per row
    sort: bool
        if true, sort the events by channel of higher energy.
    axes : np.ndarray of matplotlib Axes
        if None, create our own figure + axes
    """
    n_cols = int(np.ceil(len(events) / events_per_row))
    n_rows = min(len(events), events_per_row)

    fig, axes = plt.subplots(n_cols,
                             n_rows,
                             figsize=[1.1 * n_rows, 6 * n_cols])
    if len(events) == 1:
        axes = [axes]
    axes = np.ravel(axes)

    scale = max(np.abs(np.min(events)), np.abs(np.max(events)))

    # setting order overrides sorting
    if order is not None:
        order = order
    else:  # if order is None
        if sort:
            order = np.argsort(np.argmax(np.var(events, axis=1), axis=1))
        else:
            order = range(0, len(events))

    if labels is not None:
        assert len(labels) == len(events), "number of labels (" + str(
            len(labels)) + ") must equal number of MUAP waveforms (" + str(
                len(events)) + ")"

    for ii in range(len(events)):
        event = events[order[ii]].T / scale
        event += np.arange(
            event.shape[1]) * 0.8  # place each waveform on a separate line
        axes[ii].plot(event, c='k')
        axes[ii].set_xticks([event.shape[0] / 2])
        if labels is not None:
            axes[ii].set_xticklabels([labels[order[ii]]], fontSize=12)
        else:
            axes[ii].set_xticklabels([])
        axes[ii].set_yticklabels([])
        axes[ii].tick_params(axis='y', length=0, pad=10)
        axes[ii].tick_params(axis='x', length=0, pad=10)
        sns.despine(left=True, bottom=True)

    # turn off the remaining axes
    for ii in range(len(events), len(axes)):
        axes[ii].set_visible(False)

    if title is not None:
        assert isinstance(title, str), "title must be a string"
        plt.suptitle(title)

    if save:
        if filename is None:
            raise ValueError("must provide filename if saving")
        else:
            fig.savefig(filename, dpi=200, transparent=True, frameon=False)

    return fig, axes


def plot_stacked_events(stacks,
                        events_per_row=10,
                        sort=True,
                        labels=None,
                        title=None,
                        colors=None,
                        save=False,
                        filename=None):
    """
    Plot stacks of events on a single plot.

    Parameters
    ----------
    stacks: list of lists of snapshots (np.ndarrays)
        each template has a shape
        (n_electrodes x n_samples)
    events_per_row: int
        number of spikes to plot on each row
    sort: bool
        if true, sort the events by channel of higher energy.
    axes : np.ndarray of matplotlib Axes
        if None, create our own figure + axes
    """
    n_cols = int(np.ceil(len(stacks) / events_per_row))
    n_rows = min(len(stacks), events_per_row)
    n_ch, n_t = stacks[0][0].shape
    t_half = int(n_t // 2)

    fig, axes = plt.subplots(n_cols, n_rows, figsize=[3, 10])
    if len(stacks) == 1:
        axes = [axes]
    axes = np.ravel(axes)

    scale = np.max([np.max(np.abs(ss)) for s in stacks for ss in s])

    if labels is not None:
        assert len(labels) == len(stacks), "number of labels (" + str(
            len(labels)) + ") must equal number of MUAP waveforms (" + str(
                len(stacks)) + ")"

    for ss, stack in enumerate(stacks):
        for ii, s in enumerate(stack):
            s = s.T
            s = s / scale
            s += np.arange(
                s.shape[1])  # place each waveform on a separate line
            if colors is None:
                axes[ss].plot(s, color='k', alpha=0.8)
            else:
                axes[ss].plot(s, color=colors[ii], alpha=0.8)
            axes[ss].set_xticks([s.shape[0] / 2])
            if labels is not None:
                axes[ss].set_xticklabels([labels[ss]], fontSize=12)
            else:
                axes[ss].set_xticklabels([])
            axes[ss].set_yticklabels([])
            axes[ss].tick_params(axis='y', length=0, pad=10)
            axes[ss].tick_params(axis='x', length=0, pad=10)
            sns.despine(left=True, bottom=True)

        if labels is not None:
            axes[ss].set_xticks([t_half])
            axes[ss].set_xticklabels([labels[ss]], fontSize=12)
        else:
            axes[ss].set_xticklabels([])
        axes[ss].tick_params(axis='y', length=0, pad=0)
        axes[ss].tick_params(axis='x', length=0, pad=0)
        sns.despine(left=True, bottom=True)
        axes[ss].set_ylim([-2, 17])
        axes[ss].set_yticks(np.arange(n_ch))
        axes[ss].set_yticklabels(np.arange(0, n_ch, 1))

    # turn off the remaining axes
    for ii in range(len(stacks), len(axes)):
        axes[ii].set_visible(False)

    if title is not None:
        assert isinstance(title, str), "title must be a string"
        plt.suptitle(title)

    if save:
        if filename is None:
            raise ValueError("must provide filename if saving")
        else:
            fig.savefig(filename, dpi=200, transparent=True, frameon=False)

    fig.set_tight_layout(True)
    return fig, axes