import numpy as np

kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)
}


def convert_color_temperature(img, temperature, mode='RGB'):
    r, g, b = kelvin_table[temperature]
    if mode == 'RGB':
        matrix = np.array([r / 255, g / 255, b / 255])
    elif mode == 'BGR':
        matrix = np.array([b / 255, g / 255, r / 255])
    else:
        raise ValueError
    img = img * matrix
    return img

def equal_points(ps1, ps2):
    for p1, p2 in zip(ps1, ps2):
        if p1 != p2:
            return False
    return True

def get_shift_affine(dx, dy):
    return np.array([[1, 0, dx],
                     [0, 1, dy]])

def combine_affine(Ms):
    '''
    Ms: a list of matrices, which is the return value of cv2.getAffineTransform()
    return: combined matrix, which can be used in cv2.warpAffine()
    apply Ms[-1], then Ms[-2], ..., finally Ms[0]
    '''
    M_rst = np.diag([1,1,1])
    for M in Ms:
        M_rst = M_rst @ np.vstack([M, [0,0,1]])
    return M_rst[:2].astype(np.float32)