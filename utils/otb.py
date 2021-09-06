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
    output = np.zeros(
        (pin_layout.shape[0], pin_layout.shape[1], data.shape[1]))
    for i, row in enumerate(pin_layout):
        for j, og_idx in enumerate(row):
            output[i, j, :] = data[og_idx, :]
    return output