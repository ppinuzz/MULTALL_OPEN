C     The original code calls the following 7 plotting functions which
C     are no more available. If you try to compile stagen-18.1.f as-is, 
C     the linker won't find those functions and will crash.
C     As a quick workaround, those functions are defined, but they're
C     empty - no plots, but the code won't be broken anymore.

      SUBROUTINE SELPLT(*)
      RETURN
      END

      SUBROUTINE GRFAR(*)
      RETURN
      END

      SUBROUTINE PLTAR(*)
      RETURN
      END

      SUBROUTINE XLABEL(*)
      RETURN
      END

      SUBROUTINE YLABEL(*)
      RETURN
      END

      SUBROUTINE TITLE(*)
      RETURN
      END

      SUBROUTINE BRKPLT(*)
      RETURN
      END
