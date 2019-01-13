from conans import ConanFile, CMake, tools
import os
import shutil
import glob


class ImguisfmlConan(ConanFile):
    name = "imgui-sfml"
    version = "1.66b"  # Version of the imgui-library

    # Commit of the ImGUI-SFML library -> its master is kept up to date with
    # ImGUI releases, but it does not have proper releases. Therefore, here we
    # add a commit version that works with the used ImGUI version
    imgui_sfml_commit = "e5bc24e748c6732baa05c6be04bbd984d4159e60"
    license = "MIT"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-imgui-sfml"
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
        # Download ImGUI
        tools.get("https://github.com/ocornut/imgui/archive/v{}.zip".format(self.version))
        os.rename("imgui-{}".format(self.version), "imgui-sources")

        # Clone Imgui
        # imgui_git = tools.Git(folder="imgui")
        # imgui_git.clone("https://github.com/ocornut/imgui.git", 'v{0}'.format(self.version))


        # tools.get("https://github.com/eliasdaler/imgui-sfml/archive/v.{}.zip".format(self.version_imgui_sfml))
        # os.rename("imgui-sfml-v.{}".format(self.version_imgui_sfml), "imgui-sfml-sources")

        # Clone Imgui-SFML
        imgui_sfml_git = tools.Git(folder="imgui-sfml-sources")
        imgui_sfml_git.clone("https://github.com/eliasdaler/imgui-sfml.git")
        imgui_sfml_git.checkout(self.imgui_sfml_commit)

        # Create the source folder where all files will be moved to
        os.mkdir("sources")

        # Copy all files from imgui-sources to sources folder
        for file_name_and_path in glob.glob("imgui-sources/*.h") + glob.glob("imgui-sources/*.cpp"):
            file_name = os.path.split(file_name_and_path)[-1]
            shutil.copy(file_name_and_path, os.path.join("sources", file_name))

        # Copy all files from imgui-sfml-sources to sources folder
        for file_name_and_path in glob.glob("imgui-sfml-sources/*.h") + glob.glob("imgui-sfml-sources/*.cpp"):
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
        shutil.rmtree("imgui-sources/")
        shutil.rmtree("imgui-sfml-sources/")

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
