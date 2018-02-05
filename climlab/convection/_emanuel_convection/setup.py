from __future__ import print_function
from os.path import join, abspath


def configuration(parent_package='', top_path=None):
    global config
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.fcompiler import get_default_fcompiler, CompilerNotFound

    build = True
    try:
        # figure out which compiler we're going to use
        compiler = get_default_fcompiler()
        # set some fortran compiler-dependent flags
        f90flags = []
        if compiler == 'gnu95':
            f90flags.append('-fno-range-check')
            f90flags.append('-ffree-form')
        elif compiler == 'intel' or compiler == 'intelem':
            f90flags.append('-132')
        #  Need zero-level optimization to avoid build problems with rrtmg_lw_k_g.f90
        f90flags.append('-O0')
        #  Suppress all compiler warnings (avoid huge CI log files)
        f90flags.append('-w')
    except CompilerNotFound:
        print('No Fortran compiler found, not building the RRTMG_LW radiation module!')
        build = False

    config = Configuration(package_name='_emanuel_convection', parent_name=parent_package, top_path=top_path)
    #  Build source list
    thispath = config.local_path
    sourcelist = []
    #sourcelist.append(join(thispath,'CONVECT4','convect43c.f'))
    sourcelist.append(join(thispath,'convect.f'))
    sourcelist.append(join(thispath,'Driver.f90'))
    if build:
        config.add_extension(name='_emanuel_convection',
                             sources=sourcelist,
                             extra_f90_compile_args=f90flags,
                             f2py_options=['--quiet'],
                             )
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
