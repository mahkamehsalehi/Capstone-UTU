
import numpy as np

def get_bounding_box(segment):
    # Convert list to numpy array if it's not already
    segment = np.array(segment)

    min_values = np.min(segment, axis=0)   # minimum values along each column
    max_values = np.max(segment, axis=0)   # maximum values along each column

    bounding_box = np.concatenate((min_values, max_values))  # concatenate min and max values
    return bounding_box.tolist()  # convert numpy array back to list for Pythonic compatibility

