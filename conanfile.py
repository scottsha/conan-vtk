import os
from conans import ConanFile, CMake, tools

class vtkConan(ConanFile):
    name = "vtk"
    version = "9.2.0.a"
    source_version = "9.2.0.rc"
    short_version = "9.2"
    homepage = "https://www.vtk.org/"
    git_hash = "8eac8f81aef4ff4cfce009b7b31b0be7bfed59ad"
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
            self.options.shared = True

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON " if self.options.shared else "OFF"
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        # self.cpp_info.libdirs = ["",""]
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version
        ]