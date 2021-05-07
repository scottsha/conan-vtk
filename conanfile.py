from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool
import os
import shutil


# IMPORTANT NOTE: Even though this is a conan recipe to install VTK, when
# consuming this recipe you should still call find_package for the VTK library
# in order to have the ${VTK_USE_FILE} variable in CMake that you should
# include according with VTK documentation. This is necessary such that vtk
# libraries with factories are properly initialized. Without an
# "INCLUDE(${VTK_USE_FILE})" in your CMakeLists file you will still be able to
# compile and link with VTK, but when running the executable you will get an
# error. Note, however, that you can utill use conan for the
# target_link_libraries as usual in your CMakeLists file.


class vtkConan(ConanFile):
    name = "vtk"
    version = "9.0"
    source_version = "9.0.1"
    short_version = "9.0"
    homepage = "https://www.vtk.org/"
    git_hash = "d6710ec6fd105ee0662c80b08a6fc0cd335e11f8"
    license = "BSD license"
    url = "https://github.com/bilke/conan-vtk"
    description = "The Visualization Toolkit (VTK) is an open-source, \
        freely available software system for 3D computer graphics, \
        image processing, and visualization."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "qt": [True, False], "mpi": [True, False],
               "fPIC": [True, False], "minimal": [True, False], "ioxml": [True, False],
               "mpi_minimal": [True, False]}
    default_options = ("shared=False", "qt=False", "mpi=False", "fPIC=False",
                       "minimal=True", "ioxml=False", "mpi_minimal=False")
    generators = "cmake"
    no_copy_source = True
    source_folder = "vtk_source"
    required_modules = ["vtkCommonColor"
                        "vtkCommonComputationalGeometry",
                        "vtkCommonCore",
                        "vtkCommonDataModel",
                        "vtkCommonExecutionModel",
                        "vtkCommonMath",
                        "vtkCommonMisc",
                        "vtkCommonSystem",
                        "vtkCommonTransforms",
                        "vtkFiltersCore",
                        "vtkFiltersExtraction",
                        "vtkFiltersGeneral",
                        "vtkFiltersGeometry",
                        "vtkFiltersImaging",
                        "vtkFiltersPoints",
                        "vtkFiltersReebGraph",
                        "vtkFiltersTopology",
                        "vtkInfovisCore",
                        "vtkInfovisBoost",
                        "vtkInfovisBoostGraphAlgorithms",
                        "vtkInfovisLayout",
                        "vtkIOCore",
                        "vtkIOInfovis",
                        "vtkIOMovie",
                        "vtkIOLegacy",
                        "vtkIOGeometry",
                        "vtkIOLegacy",
                        "vtkRenderingCore"
                        "vtkViewsCore",
                        "vtkViewsGeovis",
                        "vtkViewsInfovis"]

    def source(self):
        if not os.path.isfile(self.source_folder):
            self.run("git clone https://gitlab.kitware.com/vtk/vtk.git " + self.source_folder)
        self.run("cd " + self.source_folder + " && git checkout " + self.git_hash)

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="lib", src="lib")

    def system_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            if os_info.linux_distro == 'arch':
                package_names = ["freeglut", "libxt"]
            else:
                package_names = [
                    "freeglut3-dev", "mesa-common-dev", "mesa-utils-extra",
                    "libgl1-mesa-dev", "libglapi-mesa"]

            for name in package_names:
                installer.install(name)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include/vtk-{}".format(self.version[:-2])]

        self.cpp_info.defines = ["vtkDomainsChemistry_AUTOINIT=1(vtkDomainsChemistryOpenGL2)",
         "vtkIOExport_AUTOINIT=1(vtkIOExportOpenGL2)",
         "vtkRenderingContext2D_AUTOINIT=1(vtkRenderingContextOpenGL2)",
         "vtkRenderingCore_AUTOINIT=3(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingOpenGL2)",
         "vtkRenderingOpenGL2_AUTOINIT=1(vtkRenderingGL2PSOpenGL2)",
         "vtkRenderingVolume_AUTOINIT=1(vtkRenderingVolumeOpenGL2)"]


    def build(self):
        cmake = CMake(self)
        for vtkModule in self.required_modules:
            cmake.definitions[vtkModule + "_DEFAULT"] = "ON"
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.options.minimal:
            cmake.definitions["VTK_Group_StandAlone"] = "OFF"
            cmake.definitions["VTK_Group_Rendering"] = "OFF"
        if self.options.ioxml:
            cmake.definitions["Module_vtkIOXML"] = "ON"
        if self.options.qt:
            cmake.definitions["VTK_Group_Qt"] = "ON"
            cmake.definitions["VTK_QT_VERSION"] = "5"
            cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN"] = "OFF"
        if self.options.mpi:
            cmake.definitions["VTK_Group_MPI"] = "ON"
            cmake.definitions["Module_vtkIOParallelXML"] = "ON"
        if self.options.mpi_minimal:
            cmake.definitions["Module_vtkIOParallelXML"] = "ON"
            cmake.definitions["Module_vtkParallelMPI"] = "ON"
        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
            "include/vtk-%s/vtknetcdf/include" % self.short_version,
            "include/vtk-%s/vtknetcdfcpp" % self.short_version
        ]
