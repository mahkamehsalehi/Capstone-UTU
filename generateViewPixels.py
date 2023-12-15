
import numpy as np

def generate_view_pixels(center, max_radius, num_of_rows, num_of_columns):
    """
    This function generates all view pixels for a given center, maximum radius, number of rows and columns.

    Parameters:
        center (numpy array): The center coordinates from where the view pixels are generated.
        max_radius (float): Maximum distance in which to generate the view pixels.
        num_of_rows (int): Number of rows in the grid.
        num_of_columns (int): Number of columns in the grid.

    Returns:
        indices (numpy array): Indices of the view pixels in the pixel coordinates matrix.
        pixel_coordinates (numpy array): Coordinates of all view pixels.

    """

    # Calculate total number of elements, i.e., rows * columns
    total_elements = num_of_rows * num_of_columns
    print(total_elements)
    # Initialize a matrix to store pixel coordinates with zeros
    pixel_coordinates = np.zeros((total_elements, 2))

    counter = 0
    for i in range(1,num_of_rows+1):
        for j in range(1,num_of_columns+1):
            # Increment the counter and store pixel coordinates in matrix
            counter += 1
            pixel_coordinates[counter-1] = [i,j]

    # Calculate distances between each pixel coordinate and center point
    distances = np.linalg.norm(pixel_coordinates - np.ones((total_elements,1)) * center, 2, axis=1)

    # Find indices of pixels which are within the maximum radius from the center
    indices = np.where(distances <= max_radius)[0]

    # Restrict pixel coordinates to only include view pixels (those inside the maximum radius)
    pixel_coordinates = pixel_coordinates[indices]

    return indices, pixel_coordinates

