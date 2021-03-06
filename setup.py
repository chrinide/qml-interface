import sys
from numpy.distutils.core import Extension, setup

from mkldiscover import mkl_exists

__author__ = "QML Authors"
__copyright__ = "Copyright 2016"
__credits__ = ["PLZ CITE"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Anders S. Christensen"
__email__ = "andersbiceps@gmail.com"
__status__ = "Beta"
__description__ = "Quantum Machine Learning"
__url__ = "https://github.com/qmlcode/qml"


FORTRAN = "f90"

# GNU (default)
COMPILER_FLAGS = ["-O3", "-fopenmp", "-m64", "-march=native", "-fPIC", 
                    "-Wno-maybe-uninitialized", "-Wno-unused-function", "-Wno-cpp"]
LINKER_FLAGS = ["-lgomp"]
MATH_LINKER_FLAGS = ["-lblas", "-llapack"]

# UNCOMMENT TO FORCE LINKING TO MKL with GNU compilers:
if mkl_exists(verbose=True):
    LINKER_FLAGS = ["-lgomp", " -lpthread", "-lm", "-ldl"]
    MATH_LINKER_FLAGS = ["-L${MKLROOT}/lib/intel64", "-lmkl_rt"]

# For clang without OpenMP: (i.e. most Apple/mac system)
if sys.platform == "darwin" and all(["gnu" not in arg for arg in sys.argv]):
    COMPILER_FLAGS = ["-O3", "-m64", "-march=native", "-fPIC"]
    LINKER_FLAGS = []
    MATH_LINKER_FLAGS = ["-lblas", "-llapack"]


# Intel
if any(["intelem" in arg for arg in sys.argv]):
    COMPILER_FLAGS = ["-xHost", "-O3", "-axAVX", "-qopenmp"]
    LINKER_FLAGS = ["-liomp5", " -lpthread", "-lm", "-ldl"]
    MATH_LINKER_FLAGS = ["-L${MKLROOT}/lib/intel64", "-lmkl_rt"]




ext_fkernels = Extension(name = 'qml.ml.kernels.fkernels',
                          sources = ['qml/ml/kernels/fkernels.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_farad_kernels = Extension(name = 'qml.ml.arad.farad_kernels',
                          sources = ['qml/ml/arad/farad_kernels.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_frepresentations = Extension(name = 'qml.ml.representations.frepresentations',
                          sources = ['qml/ml/representations/frepresentations.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = MATH_LINKER_FLAGS + LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fdistance = Extension(name = 'qml.ml.kernels.fdistance',
                          sources = ['qml/ml/kernels/fdistance.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fslatm = Extension(name = 'qml.ml.representations.fslatm',
                          sources = ['qml/ml/representations/fslatm.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fsolvers = Extension(name = 'qml.ml.math.fsolvers',
                          sources = ['qml/ml/math/fsolvers.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = MATH_LINKER_FLAGS + LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])



# use README.md as long description
def readme():
    with open('README.md') as f:
        return f.read()

def setup_qml():

    setup(

        name="qml",
        packages=[
            'qml',
            'qml.data',
            'qml.ml',
            'qml.ml.arad',
            'qml.ml.kernels',
            'qml.ml.math',
            'qml.ml.representations',
            'qml.models',
            ],

        # metadata
        version=__version__,
        author=__author__,
        author_email=__email__,
        platforms = 'Any',
        description = __description__,
        long_description = readme(),
        keywords = ['Machine Learning', 'Quantum Chemistry'],
        classifiers = [],
        url = __url__,

        # set up compiled package contents
        ext_modules = [
              ext_fkernels,
              ext_frepresentations,
              ext_fslatm,
              ext_fsolvers,
              ext_fdistance,
              ext_farad_kernels,
        ],
)

if __name__ == '__main__':

    setup_qml()
