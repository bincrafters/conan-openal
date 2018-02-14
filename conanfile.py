from conans import CMake, ConanFile, tools
import os


class OpenALConan(ConanFile):
    name = "openal"
    version = "1.18.2"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "http://github.com/bincrafters/conan-openal"
    license = "MIT"
    description = "OpenAL Soft is a software implementation of the OpenAL 3D audio API."

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("libalsa/1.1.5@conan/stable")

    @property
    def folder_name(self):
        return "openal-soft-openal-soft-%s" % self.version

    def source(self):
        zip_name = "%s-soft-%s.tar.gz" % (self.name, self.version)
        tools.get("https://github.com/kcat/openal-soft/archive/%s" % zip_name, md5="fa2cb3df766ab5976c86efbcc1d24d68")
        tools.replace_in_file(os.path.join(self.folder_name, "CMakeLists.txt"),
                              "PROJECT(OpenAL)",
                              '''PROJECT(OpenAL)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.folder_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib", links=True)
        self.copy("*", dst="bin", src="install/bin")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["OpenAL32"]
        else:
            self.cpp_info.libs = ["openal"]
