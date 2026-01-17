# MULTALL_OPEN 20.9 #

- Prof. John Denton's `MULTALL-OPEN` turbomachinery design system
- Version 20.9 as downloaded on 25/11/2025 from the [MULTALL-OPEN website](https://sites.google.com/view/multall-turbomachinery-design/home?authuser=0)

| Program 			| Version |
|-------------------|---------|
| `meangen` 	 	| 17.4 	  |
| `stagen`  	 	| 18.1 	  |
| `multall-open` 	| 21.3 	  |

## A few comments regarding the inputs ##
- `machine_flow_type`: 
	- `axial`: axial flow machine with a constant radius at a fixed spanwise position on each stage and with repeating flow conditions
	- `mixed`: mixed flow machine with significant changes in radius through a stage
- `rotation_speed`: since blade rotation must be in the positive theta direction, only positive values are accepted (i.e. you cannot use a negative rotation speed to mimic a rotor rotating in the opposite direction)
- `velocity_triangles_method`: method used to specify the velocity triangle
	- `A`: specify reaction degree, flow coefficient and stage loading coefficient
	- `B`: specify flow coefficient, stator exit angle and rotor exit angle
	- `C`: specify flow coefficient, rotor inlet angle and rotor exit angle
	- `D`: specify stage reaction degree, first blade row inlet angle and first blade row exit angle

## Directories content ##

| Directory | Content                                              |
|-----------|------------------------------------------------------|
| `Denton`  | Denton's original code, taken as-is from the website |


## Changes w.r.t. the original code ##
- In `meangen-17.4.f`, I've commented out line 61:
```fortran
OPEN(UNIT=5,  FILE= '/dev/tty')
```
since `'/dev/tty'` doesn't exist on Windows (there are ways to have it patched to `CON` on Windows, but it's unnecessarily complicated)


## How to compile the code ##
1. Run
```bash
gfortran -std=legacy -o MEANGEN.exe meangen-17.4.f
```
from within `Denton/multall-open/MEANGEN/meangen-program`
2. Copy the executable `MEANGEN.exe` to `pyMULTALL/bin`


## Case structure ##
- Each case must be contained in a separate directory (e.g. `CASE_DIR`)
- In `CASE_DIR`, you must have MEANGEN's input file, named `meangen.in`
```
CASE_DIR/
|-- meangen.in
```


## Input selection process ##

```mermaid
---
title: If you're not using a file, but screen input
---
flowchart TD
    start([Start]) --> 
	comprOrTurb@{shape: decision, label: "Compressor \n or \n Turbine?"}
	comprOrTurb --> C[C]
	comprOrTurb --> T[T]
	axialOrMix@{shape: decision, label: "Axial \n or \n Mixed?"}
	refSection@{shape: decision, label: "Hub, mean or tip radius as reference?"}
	stop([Stop])

	data@[/"$$T_{t,in}, p_{t,in}, N_s, n, \dot{m}$$"/]
```