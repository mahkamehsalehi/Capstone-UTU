<p align="center">
  <img  src="https://apps.utu.fi/media/logo/UTU_logo_EN_RGB.png" />
</p>

![F.I.S.H](https://github.com/mahkamehsalehi/Capstone-UTU/blob/main/Images-for-readme/fish.png?raw=true)
# F.I.S.H. 
University of Turku Capstone course fall 2023 group 2

## What is it?

Fisheye Image Software Handling (F.I.S.H.) is a tool designed by Group 2 of the University of Turku's Capstone Course in Fall 2023/Spring 2024. This software enables the calibration of inexpensive fisheye cameras to yield images comparable to those captured by more costly camera equipment. F.I.S.H. consists of a collection of Python scripts engineered to guide users through a series of steps aimed at producing a calibration filter for any camera using a fisheye lens that is not already perfect.

## Purpose
The primary objective of F.I.S.H. is to democratize the use of fisheye cameras by providing a cost-effective solution for obtaining high-quality fisheye image data. By leveraging Python scripts and a systematic calibration process, this software allows users to achieve professional-grade results without the need for expensive camera gear. This also enables some mobile usecases that are not possible to do with more expensive gear due to the weight and size limitations of some of these applications, such as drone footage.

## 3D Checkerboard for fisheye camera calibration
A three-faced calibration grid with a checkerboard pattern was used in the fisheye camera calibration
process. Commonly a 2-dimensional grid is used, but here a 3D version was required to ensure the
whole field of view of the fisheye camera would be covered.

| Specification       | 3 x 3 checkers | 10 x 10 checkers |
|---------------------|----------------|------------------|
| Target Type         | Checkerboard   | Checkerboard     |
| Board Width [mm]    | 600            | 600              |
| Board Height [mm]   | 600            | 600              |
| Rows                | 20             | 10               |
| Columns             | 20             | 10               |
| Checker Width [mm]  | 30             | 60               |

![Checker board](https://github.com/mahkamehsalehi/Capstone-UTU/blob/production/Images-for-readme/checkerboard.png?raw=true)

![Checker board assembled](https://github.com/mahkamehsalehi/Capstone-UTU/blob/production/Images-for-readme/checkerboard2.png?raw=true)

Assembled 3D calibration checkerboard

![Checker board corner supports](https://github.com/mahkamehsalehi/Capstone-UTU/blob/production/Images-for-readme/checkerboard3.png?raw=true)

Two-slotted corner support for the center and side corners.

![Checker board front corner supports](https://github.com/mahkamehsalehi/Capstone-UTU/blob/production/Images-for-readme/checkerboard4.png?raw=true)

A support to level the front-facing lower corner.

## Prerequisites
* Python 3.10 or newer
* Video taken with a fisheye camera of a calibration checkerboard
## Installation
1. Clone the repository `git clone https://github.com/mahkamehsalehi/Capstone-UTU.git`.
2. Navigate to the cloned repository `cd Capstone-UTU`.
3. Install required Python packages with `pip install -r requirements.txt`

## Usage

To use the software you must run 4 separate scripts that can all be found at the root level of the repository.
Once you have cloned the repository and installed the required packages follow these steps in your terminal:
1. Run `python mainEditCurves.py`. This first step is where corner point registeration is done. Currently this is manual labor and takes quite some time.
3. Run `python mainFit.py`
4. Run `python mainMapping.py`
5. Run `python mainProcessFrames.py`

## Known issues

* mainFit optimizes fitting error for single frame and not set of three frames.
* mainFit calculates fitting errors on a frame-by-frame basis to optimize hyperparameters, when errors should be calculated for each set of three frames to compare hyperparameter performance. This causes the parameter optimization to be overly optimistic as the first frame seems to consistently have the lowest error. Proposed fix is to sum the errors from each of the three frames in order to have a valid point of comparison between hyperparameters.
* Corner point registration in mainFit is currently done when a frame has the smallest total error that has been found thus far. Because the first frame consistently has lower error than frames 2 and 3, corner point registration is done only for frame 1 if its total error is the smallest so far. This causes the resulting vector field to be much more sparse as only one image’s correction vectors are collected. Proposed fix is to implement the summing errors from each set of frames as described in the previous known bug and calculate corner point registration for each frame in the current minimum error set of frames.
* Weights calculated in the mainMapping are not calculated correctly. Their sum is 1 as it should be but the weights itself are the same number. For example, for four pixels the weights are all 0.25 and for two pixels the weights are 0.5. This can be seen especially well from the weight boxplots the mainMapping prints. The weights are needed for moving the pixels to their calibrated places. The problem probably arises from the bump function so it should be checked out.
* The pixel mapping operation which is done in mainProcessFrames is currently faulty. The issue is known to be caused by bad indexing of the pixel mapping operation between lines 51 and 55 of mainProcessFrames. This causes the mapped video to look like noisy static. Proposed fix is to investigate the indexing operations in the previously mentioned lines and correct the faulty indexing.

## Improvements

* **Automatic Detection of Corner Points:**
  - Corner points are currently registered by hand in `mainEditCurves.py`. This is a very labor-intensive and time-consuming process, because registering the corner points in one image takes an hour or more, depending on the registerer’s proficiency and number and severity of image imperfections. Still, the software benefits heavily from a large number of registered corner points for more accurate corrections. Therefore, the registration of corner points should be automated. There are existing implementations of automatic corner point registration that can be used as a basis for the implementation.

* **mainFit calculates unnecessary crossing point registrations:**
  - The most computationally intensive part of `mainFit.py` is the crossing point registration. Currently, this is done every time a frame has the smallest error so far. This means that corner point registration could theoretically be done 45 times with the current hyperparameter optimization. This should only ever need to be done 3 times, once for each of the frames in the input set with the optimized hyperparameters. Suggested fix is to move the corner point registration outside of the hyperparameter optimization loop and save optimized hyperparameters and other required data that are used in corner point registration.

* **Optimizing truncation parameter lambda or exploring other regularization methods:**
  - The software currently uses Fourier truncation to deal with outliers in the vector field. The degree of this truncation is governed by a single constant value. To reach a better level of truncation this parameter should be included into the hyperparameter optimization process in `mainFit`. This would allow the system to better eliminate outliers in the vector field. If Fourier truncation is found to be an inefficient method for regularization, more sophisticated methods of regularization should be implemented and optimized.

* **Improving quality of code for better readability:**
  - The naming of methods and variables can be extremely confusing at the moment. To improve readability, the commenting and naming conventions of variables and methods should be improved.

## Future work

* **Cloning and Expanding the Git Repository:**
  - The existing repository should be cloned and expanded to match the level required by an academic research project. This repository will be unaltered for preservation purposes.

* **Coding an execution pipeline:**
  - Currently, the code needs to be run as individual main methods. To make the software more user-friendly, an execution pipeline should be created to provide the user with a less arduous user experience.




