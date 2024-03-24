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

Assembeled 3D calibration checkerboard


## Features
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
1. Run `python mainEditCurves.py`
2. Run `python mainFit.py`
3. Run `python mainMapping.py`
4. Run `python mainProcessFrames.py`
