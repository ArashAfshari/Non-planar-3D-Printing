# Non-planar-3D-Printing 
This repository contains the accompanying code for the following publication:

Afshari,Tröger,Meyer,Inkermann - *Non-planar 3D Printing - Enhancing Design Potentials By Advanced Slicing Algorithms and Path Planning*

## Code Description
The code in *gcode_modifier.py* modifies a given g-code to enable non-planar printing. At first step, this code calculates the distance between two g-code lines in three dimensions and provide extrusion value based on the distance and a extrusion factor. Then it will provide a loop to do the mentioned task for all the g-code provided in the g-code example list.

## Citation
```
@article{Afshari_NonplanarPrinting_2025,
  title={Non-planar 3D Printing - Enhancing Design Potentials By Advanced Slicing Algorithms and Path Planning},
  author={Afshari, A. and Tröger, J.-A. and Meyer, J. and Inkermann, D.},
  year={2025},
  journal={Submitted to Procedia CIRP}
}
```
