# MAKEFILE TO COMPILE DENTON'S MEANGEN, STAGEN AND MULTALL

FORTRAN_COMPILER = gfortran
# -std=legacy    to compile FORTRAN 77
FLAGS = -std=legacy
EXE_NAME = STAGEN.exe
SRC_FILE = stagen-18.1.f
# original plotting utilities are no more available => they've been replaced by
# a dummy library where those functions are defined, but they're empty, so that
# the code will compile and run with no erros, but not plot will be created
PLOT_LIBS = dummyplotutils.f


# ----------------------------------- RULES -----------------------------------

# default target (built when running just 'make')
all: $(EXE_NAME)

# Rule to build the executable: "to build $(EXE_NAME), i.e. STAGEM.exe, you 
# need $(SRC_FILE), i.e. stagen-18.1.f, and what follows are the instruction"
$(EXE_NAME): $(SRC_FILE)
	$(FORTRAN_COMPILER) $(FLAGS) -o $(EXE_NAME) $(SRC_FILE) $(PLOT_LIBS)
# fancier version:
#   $@ = target name (MEANGEN.exe)
#   $< = first dependency (stagen-18.1.f)
#	$(FORTRAN_COMPILER) $(FLAGS) -o $@ $<

# remove compiled executable
clean:
	rm -f $(EXE_NAME)

# specify that 'all' and 'clean' are target not associated with any file
# (so that, even if 'all' and 'clean' are existing files, make will run)
.PHONY: all clean
