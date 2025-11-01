from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import copy
import os


class BreakpadConan(ConanFile):
    name = "breakpad"
    version = "2024.02.16"
    license = "BSD-3-Clause"
    author = "Google"
    url = "https://github.com/google/breakpad"
    description = "A set of client and server components which implement a crash-reporting system"
    topics = ("crash-reporting", "minidump", "debugging")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_processor": [True, False],
        "build_client": [True, False],
        "build_tools": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_processor": True,
        "build_client": True,
        "build_tools": False
    }
    exports_sources = "CMakeLists.txt", "Config.cmake.in", "breakpad-2024.02.16/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BREAKPAD_BUILD_PROCESSOR"] = self.options.build_processor
        tc.variables["BREAKPAD_BUILD_CLIENT"] = self.options.build_client
        tc.variables["BREAKPAD_BUILD_TOOLS"] = self.options.build_tools
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", 
             src=os.path.join(self.source_folder, "breakpad-2024.02.16"),
             dst=os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        # 客户端库
        if self.options.build_client:
            self.cpp_info.components["client"].libs = ["breakpad_client"]
            self.cpp_info.components["client"].includedirs = ["include"]
            
            if self.settings.os == "Windows":
                self.cpp_info.components["client"].system_libs = ["wininet", "dbghelp"]
            elif self.settings.os == "Linux":
                self.cpp_info.components["client"].system_libs = ["pthread"]
            elif self.settings.os == "Macos":
                self.cpp_info.components["client"].frameworks = ["Foundation"]

        # 处理器库
        if self.options.build_processor:
            self.cpp_info.components["processor"].libs = ["breakpad_processor"]
            self.cpp_info.components["processor"].includedirs = ["include"]
            
            if self.settings.os == "Windows":
                self.cpp_info.components["processor"].system_libs = ["imagehlp", "dbghelp"]
            elif self.settings.os == "Linux":
                self.cpp_info.components["processor"].system_libs = ["pthread"]
