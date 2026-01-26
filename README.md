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

3. (Optional) compile the docs in HTML by running `make html` from within `docs`


## Case structure ##
- Each case must be contained in a separate directory (e.g. `CASE_DIR`)
- In `CASE_DIR`, you must have MEANGEN's input file, named `meangen.in`
```
CASE_DIR/
|-- meangen.in
```


## Original MEANGEN flowchart ##

```mermaid
graph TD
     input@{shape: manual-input, label: "User Input"} 
     --> lab1100@{shape: rect, label: "1100"}
     --> CandAXI@{shape: decision, label: "IFSAME_ALL == 'C' \n and \n FLO_TYP == 'AXI'?"}
     --YES--> a@{shape: rect, label: "FLOW_TYP = 'MIX'"} --> lab2000@{shape: rect, label: "2000"}
     CandAXI --NO--> CandMIX@{shape: decision, label: "IFSAME_ALL == 'C' \n and \n FLO_TYP == 'MIX'?"}
     --YES--> b@{shape: rect, label: "FLOW_TYP = 'AXI' \n and \n MIX_TYP = 'N'"} --> lab500@{shape: rect, label: "500"}
     CandMIX --NO--> AXIY@{shape: decision, label: "FLOW_TYP = 'AXI' \n and \n IFSAME_ALL = 'Y'"}
     --NO--> MIXY@{shape: decision, label: "FLOW_TYP = 'MIX' \n and \n IFSAME_ALL = 'Y'"}
     AXIY --YES--> lab600@{shape: rect, label: "600"}
     MIXY --NO--> lab500
     MIXY --YES--> lab700@{shape: rect, label: "700"}
     lab500 --> MIX@{shape: decision, label: "FLOW_TYP = 'MIX'?"}
     MIX --YES--> lab2000
     MIX --NO--> INTYPE@{shape: decision, label: "INTYPE?"}
	 --A--> inputA["$$\chi, \phi, \psi$$"]
	 INTYPE --B--> inputB["$$\phi, \alpha_{stat}^{out}, \alpha_{rot}^{out}$$"]
	 INTYPE --C--> inputC["$$\phi, \theta_{rot}^{in}, \theta_{rot}^{out}$$"]
	 INTYPE --D--> inputD["$$\theta_{1st}^{in}, \theta_{1st}^{out}, \chi$$"]
	 inputA --> RADTYPE@{shape: decision, label: "RADTYPE?"}
	 inputB --> RADTYPE
	 inputC --> RADTYPE
	 inputD --> RADTYPE
	 --A--> radDes["$$R_{des}$$"]
	 RADTYPE --B--> dhstage["$$\Delta h_{stage}$$"]
	 --> cax["$$c_{ax,1}, c_{ax,2}, \Delta z_{row}, \Delta z_{stage}$$"]
	 radDes --> cax
	 --> lab600
	 lab2000 --> MIXTYP@{shape: decision, label: "MIXTYP?"}
	 MIXTYP --A--> typeA["$$\alpha_{in}, \alpha_{out}, \beta_{in}, \beta_{out}$$"]
	 MIXTYP --B--> typeB["$$\phi_{rot,LE,1st}, \alpha_{in}, \alpha_{out}, \psi$$"]
	 --> lab700
	 typeA --> lab700 --> labs130["134, 135, 136, 137, 139"]
	 --> changeStreamSurf@{shape: decision, label: "Change stream surface?"}
	 --NO--> lab3000["3000"]
	 changeStreamSurf --YES--> lab700
```