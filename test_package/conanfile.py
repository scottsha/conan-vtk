#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        print("configuring in the test script")
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.a", dst="bin", src="bin")
        self.copy("*.so*", dst="bin", src="lib")
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path)
