# MAKEFILE TO COMPILE DENTON'S MEANGEN, STAGEN AND MULTALL

FORTRAN_COMPILER = gfortran
# -std=legacy    to compile FORTRAN 77
FLAGS = -std=legacy
EXE_NAME = MEANGEN.exe
SRC_FILE = meangen-17.4.f


# ----------------------------------- RULES -----------------------------------

# default target (built when running just 'make')
all: $(EXE_NAME)

# Rule to build the executable: "to build $(EXE_NAME), i.e. MEANGEN.exe, you 
# need $(SRC_FILE), i.e. meangen-17.4.f, and what follows are the instruction"
$(EXE_NAME): $(SRC_FILE)
	$(FORTRAN_COMPILER) $(FLAGS) -o $(EXE_NAME) $(SRC_FILE)
# fancier version:
#   $@ = target name (MEANGEN.exe)
#   $< = first dependency (meangen-17.4.f)
#	$(FORTRAN_COMPILER) $(FLAGS) -o $@ $<

# remove compiled executable
clean:
	rm -f $(EXE_NAME)

# specify that 'all' and 'clean' are target not associated with any file
# (so that, even if 'all' and 'clean' are existing files, make will run)
.PHONY: all clean
