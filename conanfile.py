from conans import CMake, ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil

class OpenALConan(ConanFile):
    name = "openal"
    version = "1.18.2"
    ZIP_FOLDER_NAME = "openal-soft" + name + "-soft-" + version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bincrafters/conan-openal"
    license="MIT License"
    description="OpenAL Soft is a software implementation of the OpenAL 3D audio API."

    #def system_requirements(self):
    #    if self.settings.os == "Linux":
    #        installer = tools.SystemPackageTool()
    #        installer.install("libasound2-dev")

    def source(self):
        zip_name = "%s-soft-%s.tar.gz" % (self.name, self.version)
        tools.download("https://github.com/kcat/openal-soft/archive/%s" % zip_name, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        os.rename("openal-soft-openal-soft-1.18.2", "sources")

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-DCMAKE_INSTALL_PREFIX:PATH=../install")
        if self.options.shared == True:
            cmake_options.append("-DBUILD_SHARED_LIBS=ON")

        if self.settings.os == "Windows":
            self.run("IF not exist build mkdir build")
        else:
            self.run("mkdir build")
        cd_build = "cd build"
        self.output.warn('%s && cmake .. %s %s' % (cd_build, cmake.command_line, " ".join(cmake_options)))
        self.run('%s && cmake .. %s %s' % (cd_build, cmake.command_line, " ".join(cmake_options)))
        self.output.warn('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
        self.run('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib", links=True)
        self.copy("*", dst="bin", src="install/bin")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["OpenAL32"]
        else:
            self.cpp_info.libs = ["openal"]

