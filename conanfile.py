from   conans       import ConanFile, CMake, tools
from   distutils.dir_util import copy_tree

class BgfxConan(ConanFile):
    name            = "bgfx"
    exports_sources = "bgfx.cmake/*"
    source_folder   = "bgfx.cmake"
    description     = "Conan package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"
    options         = {
            "shared": [True, False],
            "multithreaded": [True, False]
            }
    default_options = {
            "shared": False,
            "multithreaded": True
            }

    def set_version(self):
        git = tools.Git(self.source_folder)
        self.version = git.get_tag()[1:]

    def build(self):
        cmake          = CMake(self)
        options = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "BGFX_CONFIG_MULTITHREADED": self.options.multithreaded,
            "BGFX_BUILD_EXAMPLES": False,
            "BGFX_BUILD_TOOLS": False,
            "BGFX_OPENGL_VERSION": 33
            }

        cmake.configure(None, options)
        cmake.build()

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.collect_headers("bgfx/include")
        self.collect_headers("bimg/include")
        self.collect_headers("bx/include"  )
        self.copy("*.a"  , dst="lib", keep_path=False)
        self.copy("*.so" , dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("shaderc", dst="bin")
        self.copy("*.exe", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["bgfx", "bimg", "bx"]
        self.cpp_info.libs.extend(["astc-codec", "astc", "edtaa3", "etc1", "etc2", "iqa", "squish", "pvrtc", "tinyexr", "nvtt"])
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags = ["-framework Cocoa", "-framework QuartzCore", "-framework OpenGL", "-weak_framework Metal"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["GL", "X11", "pthread", "dl"])
        if self.settings.os == "Windows":
            self.cpp_info.includedirs = ["include", "include/compat/msvc"]
