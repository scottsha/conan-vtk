from pathlib import Path

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import get, replace_in_file, save
from conan.tools.system.package_manager import Apt


class vtkRecipe(ConanFile):
    name = "vtk"
    user = "ss"
    channel = "testing"

    # Optional metadata
    license = "BSD license"
    url = "https://github.com/darcamo/conan-vtk"
    description = "The Visualization Toolkit (VTK) is an open-source, \
        freely available software system for 3D computer graphics, \
        image processing, and visualization."
    topics = ("3D", "visualization", "graphics")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "wrap_python": [True, False], "use_mpi": [True, False]}
    default_options = {"shared": False, "fPIC": True, "wrap_python": False, "use_mpi": False}

    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def system_requirements(self):
        apt = Apt(self)
        apt.install(["libglvnd-dev"])

    def requirements(self):
        self.requires("expat/[~2]", transitive_headers=True, transitive_libs=True)
        self.requires("nlohmann_json/[~3]", transitive_headers=True, transitive_libs=True)

    def source(self):
        get(self, self.conan_data["sources"][self.version], strip_root=True)
        replace_in_file(
            self, Path(self.source_folder) / "ThirdParty/expat/CMakeLists.txt", "EXPAT::EXPAT", "expat::expat"
        )
        save(
            self,
            path=Path(self.source_folder) / "CMakeLists.txt",
            append=True,
            content="""
add_library(vtk_conan_all_modules INTERFACE)
target_link_libraries(vtk_conan_all_modules INTERFACE ${vtk_modules})
install(TARGETS vtk_conan_all_modules EXPORT "${vtk_install_export}")
""",
        )

    def config_options(self):  # noqa: D102
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):  # noqa: D102
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):  # noqa: D102
        cmake_layout(self)

    def generate(self):  # noqa: D102
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.cache_variables["VTK_WRAP_PYTHON"] = self.options.wrap_python
        tc.cache_variables["VTK_USE_MPI"] = self.options.use_mpi
        tc.cache_variables["VTK_MODULE_ENABLE_VTK_WrappingPythonCore"] = "YES" if self.options.wrap_python else "NO"
        tc.cache_variables["VTK_MODULE_ENABLE_VTK_Python"] = "YES" if self.options.wrap_python else "NO"
        tc.cache_variables["VTK_MODULE_USE_EXTERNAL_VTK_nlohmannjson"] = True
        tc.variables["VTK_MODULE_USE_EXTERNAL_VTK_expat"] = True
        tc.generate()

    def build(self):  # noqa: D102
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):  # noqa: D102
        cmake = CMake(self)
        cmake.install()

    def package_info(self):  # noqa: D102
        # NOTE: This will only work for consumers using the CMakeDeps
        # and CMakeToolchain generators. Also, in consumers
        # CMakeLists.txt file they need to link with VTK using
        # something like
        #
        #    target_link_libraries(myexe PRIVATE ${VTK_LIBRARIES})
        #
        # and include the code below after that
        #
        #     include(vtkModule)
        #     # vtk_module_autoinit is needed
        #     vtk_module_autoinit(
        #         TARGETS example
        #         MODULES ${VTK_LIBRARIES}
        #     )
        #
        # This is how VTK is consumed in the VTK examples when it is
        # installed in the system.

        # Tell Conan CMakeDeps generator in the consumers to NOT
        # generate the config files for VTK
        self.cpp_info.set_property("cmake_find_mode", "none")
        # For transitive dependencies Conan still seems to rely on these properties. The defaults are not working.
        self.cpp_info.set_property("cmake_file_name", "VTK")
        # This fix relies on the patched CMake script above to provide the "all" target.
        # The issues is related to the usage of CMake targets when VTK becomes a transitive dependency.
        # For transitive dependencies Conan seems to be relying on the below property.
        self.cpp_info.set_property("cmake_target_name", "VTK::vtk_conan_all_modules")
        # This will add the folder where VTK installed its cmake
        # config files to the CMAKE_PREFIX_PATH variable in the
        # consumer.
        two_digit_version = self.version[:-2]
        assert len(two_digit_version) == 3
        self.cpp_info.builddirs = [f"lib/cmake/vtk-{two_digit_version}"]
