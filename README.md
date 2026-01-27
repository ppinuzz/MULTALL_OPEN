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
since `'/dev/tty'` doesn't exist on Windows (there are ways to have it patched to `CON` on Windows, but it's unnecessarily complicated).
Another possibility would be to replace `'/dev/tty'` with `CON`, but then that code would work only on Windows
The line of code forces stream `5` (which is always STDIN) to read from the terminal you typed in (always referenced by `/dev/tty`), ensuring that the program could always ask for user input even if STDIN was redirected. Since it's not strictly necessary, you can remove it for a quick fix.
- STAGEN calls some plotting utilities which are no more available, therefore trying to compile `stagen-18.1.f` will result in a linker error. To quickly fix this with zero-to-no modifications, the 7 plot functions have been defined as "empty functions" in a `dummyplotutils.f` file, which is compiles as-if it were the missing library. The 7 function names have been obtained by trying to compile the code on WSL, which returned the error
```
/usr/bin/ld: /tmp/ccO3APyB.o: in function `MAIN__':
stagen-18.1.f:(.text+0xf32e): undefined reference to `selplt_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf36a): undefined reference to `grfar_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf39f): undefined reference to `pltar_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf3bd): undefined reference to `xlabel_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf3db): undefined reference to `ylabel_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf420): undefined reference to `title_'
/usr/bin/ld: stagen-18.1.f:(.text+0xf42e): undefined reference to `brkplt_'
```
The missing functions are, therefore, `SELPLT`, `GRFAR`, `PLTAR`, `XLABEL`, `YLABEL`, `TITLE`, `BRKPLT`. Each dummy function is defined, e.g., as
```fortran
SUBROUTINE SELPLT(*)
	RETURN
END
```
Anything that is passed to the function either read and not used, or discarded. Potentially unsafe.


## How to compile the code ##
1. Run
```bash
gfortran -std=legacy -o MEANGEN.exe meangen-17.4.f
```
from within `Denton/multall-open/MEANGEN/meangen-program`

2. Copy the executable `MEANGEN.exe` to `pyMULTALL/bin`

3. (Optional) compile the docs in HTML by running `make html` from within `docs`

4. Run
```bash
gfortran -std=legacy -o STAGEN.exe stagen-18.1.f dummyplotutils.f
```
from within `Denton/multall-open/MEANGEN/stagen-program`

## Case structure ##
- Each case must be contained in a separate directory (e.g. `CASE_DIR`)
- In `CASE_DIR`, you must have MEANGEN's input file, named `meangen.in`
```
CASE_DIR/
|-- meangen.in
```

