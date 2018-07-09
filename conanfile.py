from conans import ConanFile, CMake, tools
import os
import shutil
import glob


class ImguisfmlConan(ConanFile):
    name = "imgui-sfml"
    version = "1.53"  # Version of the imgui-library
    version_imgui_sfml = ".1.0"  # Version of imgui-sfml corresponding to the
                                 # version of imgui that it works with
    license = "MIT"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = (
        "Dear ImGui: Bloat-free Immediate Mode Graphical User "
        "interface for C++ with minimal dependencies. This conan "
        "package also install the imgui-sfml to use imgui with SFML."
        "\nSee https://github.com/eliasdaler/imgui-sfml")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    def system_requirements(self):
        sfml_package_name = None
        if tools.os_info.linux_distro == "ubuntu":
            sfml_package_name = "libsfml-dev"
        elif tools.os_info.linux_distro == "arch":
            sfml_package_name = "sfml"

        if sfml_package_name:
            installer = tools.SystemPackageTool()
            installer.install(sfml_package_name)

    def source(self):
        # Clone Imgui
        imgui_git = tools.Git(folder="imgui")
        imgui_git.clone("https://github.com/ocornut/imgui.git", 'v{0}'.format(self.version))

        # Clone Imgui-SFML
        imgui_sfml_git = tools.Git(folder="imgui-sfml")
        imgui_sfml_git.clone("https://github.com/eliasdaler/imgui-sfml.git", 'v{0}'.format(self.version_imgui_sfml))

        # Create the source folder where all files will be moved to
        os.mkdir("sources")
        for file_name_and_path in glob.glob("imgui/*.h") + glob.glob("imgui/*.cpp"):
            file_name = os.path.split(file_name_and_path)[-1]
            shutil.copy(file_name_and_path, os.path.join("sources", file_name))
        for file_name_and_path in glob.glob("imgui-sfml/*.h") + glob.glob("imgui-sfml/*.cpp"):
            file_name = os.path.split(file_name_and_path)[-1]
            shutil.copy(file_name_and_path, os.path.join("sources", file_name))

        # Now all relevant files are in the sources folder. We still need to
        # append the content of sources/imconfig-SFML.h to sources/imconfig.h
        # and remove sources/imconfig-SFML.h
        imconfig_content = tools.load("sources/imconfig.h")
        imconfig_sfml_content = tools.load("sources/imconfig-SFML.h")
        concatenated_content = "{0}\n\n{1}".format(imconfig_content, imconfig_sfml_content)
        tools.save("sources/imconfig.h", concatenated_content)

        # Now we can remove the imgui and imgui-sfml folders
        shutil.rmtree("imgui/")
        shutil.rmtree("imgui-sfml/")

        # In case of ubuntu find_package will not find SFML unless we indicate
        # to cmake where to find the FindSFML.cmake file
        if (tools.os_info.linux_distro == 'ubuntu'):
            tools.replace_in_file(
                "CMakeLists.txt",
                "# PLACEHOLDER",
                ('# Add a folder to CMAKE_MODULE_PATH to indicate where the '
                 'SFML module can be found\nlist(APPEND CMAKE_MODULE_PATH '
                 '"/usr/share/SFML/cmake/Modules")'))
        else:
            tools.replace_in_file(
                "CMakeLists.txt",
                "# PLACEHOLDER",
                "")

        # Copy the CMakeLists.txt file to the sources folder
        shutil.move("CMakeLists.txt", "sources/")

    def build(self):
        os.mkdir("build")
        cmake = CMake(self)
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

    def package_info(self):
        # self.cpp_info.libs = ["imgui-sfml"]
        self.cpp_info.libs = ["imgui-sfml", "sfml-graphics", "sfml-window", "sfml-audio", "sfml-network", "sfml-system", "GL"]
