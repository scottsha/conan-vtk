import os
from conans import ConanFile, CMake, tools


class vtkConan(ConanFile):
    name = "vtk"
    version = "9.1"
    source_version = "9.1.0"
    short_version = "9.1"
    homepage = "https://www.vtk.org/"
    git_hash = "285daeedd58eb890cb90d6e907d822eea3d2d092"
    url = "https://github.com/bilke/conan-vtk"
    description = "The Visualization Toolkit (VTK) is an open-source, \
        freely available software system for 3D computer graphics, \
        image processing, and visualization."
    exports = ["LICENSE.md", "CMakeLists.txt", "FindVTK.cmake"]

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "qt": [True, False], "mpi": [True, False],
               "fPIC": [True, False], "minimal": [True, False], "ioxml": [True, False],
               "mpi_minimal": [True, False]}
    default_options = ("shared=True", "qt=False", "mpi=False", "fPIC=False",
                       "minimal=False", "ioxml=False", "mpi_minimal=False")
    generators = "cmake"
    no_copy_source = True
    short_paths = True
    vtk_source_folder = "vtk_source"
    # required_modules = ["vtkCommonColor"
    #                     "vtkCommonComputationalGeometry",
    #                     "vtkCommonCore",
    #                     "vtkCommonDataModel",
    #                     "vtkCommonExecutionModel",
    #                     "vtkCommonMath",
    #                     "vtkCommonMisc",
    #                     "vtkCommonSystem",
    #                     "vtkCommonTransforms",
    #                     "vtkFiltersCore",
    #                     "vtkFiltersExtraction",
    #                     "vtkFiltersGeneral",
    #                     "vtkFiltersGeometry",
    #                     "vtkFiltersImaging",
    #                     "vtkFiltersPoints",
    #                     "vtkFiltersReebGraph",
    #                     "vtkFiltersTopology",
    #                     "vtkInfovisCore",
    #                     "vtkInfovisBoost",
    #                     "vtkInfovisBoostGraphAlgorithms",
    #                     "vtkInfovisLayout",
    #                     "vtkIOCore",
    #                     "vtkIOInfovis",
    #                     "vtkIOMovie",
    #                     "vtkIOLegacy",
    #                     "vtkIOGeometry",
    #                     "vtkIOLegacy",
    #                     "vtkRenderingCore"
    #                     "vtkViewsCore",
    #                     "vtkViewsGeovis",
    #                     "vtkViewsInfovis"]

    def source(self):
        self.run("git clone -b release --single-branch https://gitlab.kitware.com/vtk/vtk.git " + self.vtk_source_folder)
        self.run("cd " + self.vtk_source_folder + " && git checkout " + self.git_hash)

    def requirements(self):
        if self.options.qt:
            self.requires("Qt/5.11.2@bincrafters/stable")
            self.options["Qt"].shared = True
            self.options["Qt"].qtxmlpatterns = True
            if tools.os_info.is_linux:
                self.options["Qt"].qtx11extras = True

    def _system_package_architecture(self):
        if tools.os_info.with_apt:
            if self.settings.arch == "x86":
                return ':i386'
            elif self.settings.arch == "x86_64":
                return ':amd64'

        if tools.os_info.with_yum:
            if self.settings.arch == "x86":
                return '.i686'
            elif self.settings.arch == 'x86_64':
                return '.x86_64'
        return ""

    def build_requirements(self):
        pack_names = None
        if not self.options.minimal and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                pack_names = [
                    "freeglut3-dev",
                    "mesa-common-dev",
                    "mesa-utils",
                    "libgl1-mesa-dev",
                    "libglapi-mesa",
                    "libsm-dev",
                    "libx11-dev",
                    "libxext-dev",
                    "libxt-dev",
                    "libglu1-mesa-dev"]

        if pack_names:
            installer = tools.SystemPackageTool()
            for item in pack_names:
                installer.install(item + self._system_package_architecture())

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.options.fPIC
        if self.settings.os == "Linux":
            self.options.fPIC = True

    def build(self):
        cmake = CMake(self)
        # -include /usr/include/c++/11/limits
        # for vtkModule in self.required_modules:
        #     cmake.definitions[vtkModule + "_DEFAULT"] = "ON"
        # cmake.definitions["BUILD_TESTING"] = "OFF"
        # cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON " if self.options.shared else "OFF"
        # if self.options.minimal:
        #     cmake.definitions["VTK_Group_StandAlone"] = "OFF"
        #     cmake.definitions["VTK_Group_Rendering"] = "OFF"
        # if self.options.ioxml:
        #     cmake.definitions["Module_vtkIOXML"] = "ON"
        # if self.options.qt:
        #     cmake.definitions["VTK_Group_Qt"] = "ON"
        #     cmake.definitions["VTK_QT_VERSION"] = "5"
        #     cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN"] = "OFF"
        # if self.options.mpi:
        #     cmake.definitions["VTK_Group_MPI"] = "ON"
        #     cmake.definitions["Module_vtkIOParallelXML"] = "ON"
        # if self.options.mpi_minimal:
        #     cmake.definitions["Module_vtkIOParallelXML"] = "ON"
        #     cmake.definitions["Module_vtkParallelMPI"] = "ON"
        #
        # if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
        #     cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        #
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs += ["dl","pthread"]
        vtk_base_include_dir = "include/vtk-%s" % self.short_version
        vtk_include_subdirs = [vtk_base_include_dir] + [foo[0] for foo in os.walk(vtk_base_include_dir)]
        self.cpp_info.includedirs = vtk_include_subdirs




    def package(self):
    # Copy the libraries
        if self.options.shared:
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
