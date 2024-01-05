import numpy.ma as ma
from scipy import stats
import scipy
import numpy as np


def array_to_probability_radar(
    array: np.ndarray, loc: float, scale: float, invert: bool = False
) -> np.ndarray:
    """Converts continuous variable into 0-1 probability.

    Args:
        array: Numpy array.
        loc: Center of the distribution. Values smaller than this will have small probability.
            Values greater than this will have large probability.
        scale: Width of the distribution, i.e., how fast the probability drops or increases from
            the peak.
        invert: If True, large values have small probability and vice versa. Default is False.

    Returns:
        Probability with the same shape as the input data.

    """
    arr = ma.copy(array)
    prob = np.zeros(arr.shape)
    ind = ~arr.mask
    if invert:
        arr *= -1
        loc *= -1
    prob[ind] = stats.norm.cdf(arr[ind], loc=loc, scale=scale)
    return prob

def subbotin(x, shape, loc, scale ):
    return (shape/(2*scale*scipy.special.gamma(1/shape)))*np.exp(-(np.abs(x-loc)/scale)**shape)

def array_to_probability_ceilometer(
    array: np.ndarray, shape: float, loc: float, scale: float, invert: bool = False
) -> np.ndarray:
    """Converts a continuous variable into a probability distribution.

    Args:
        x (numpy array): Input data.
        shape (float): Shape parameter that controls the shape of the probability distribution.
        loc (float): Center of the distribution. Values smaller than this will have a small probability,
            and values greater than this will have a larger probability.
        scale (float): Width of the distribution, determining how fast the probability drops or increases
            from the peak.

    Returns:
        Probability (numpy array): A probability distribution with the same shape as the input data.

    """
    arr = ma.copy(array)
    prob = np.zeros(arr.shape)
    ind = ~arr.mask
    if invert:
        arr *= -1
        loc *= -1
    prob[ind] = subbotin(arr[ind], shape, loc, scale )
    # Normalize probabilities to range [0, 1]
    prob /= prob.max()

    return prob

def replace_with_new_value_conditional(target_classification, combined_probability, height, new_value, cloud_base_height, prob_thresh):
    array1 = target_classification.T
    array2 = combined_probability
    cbh    = cloud_base_height
    height_index = None
    for i in range(len(cbh)):
        if cbh[i] is not None and cbh[i] < 1000:
            height_index = np.where(height > cbh[i])[0][0]
        else:
            height_index = np.where(height > 2000)[0][0]

        if height_index is not None:
            array1[(array2 > prob_thresh) & (array1 == 2)] = new_value

    return array1


