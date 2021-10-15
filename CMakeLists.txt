cmake_minimum_required(VERSION 3.10)
project(imgui-sfml)

# PLACEHOLDER

find_package(SFML REQUIRED COMPONENTS system window graphics network audio)

add_library(imgui-sfml
  imconfig-SFML.h
  imconfig.h
  imgui-SFML.cpp
  imgui-SFML.h
  imgui-SFML_export.h
  imgui.cpp
  imgui.h
  imgui_demo.cpp
  imgui_draw.cpp
  imgui_internal.h
  imgui_tables.cpp
  imgui_widgets.cpp
  imstb_rectpack.h
  imstb_textedit.h
  imstb_truetype.h
  )





target_include_directories(imgui-sfml SYSTEM PUBLIC .)
target_link_libraries(imgui-sfml PUBLIC sfml-graphics sfml-window sfml-system sfml-network sfml-audio)
target_link_libraries(imgui-sfml PUBLIC "-lGL")


# Rule to install the compiled library
install(TARGETS imgui-sfml DESTINATION lib)
# Rule to install the headers
install(FILES
  imconfig.h
  imgui-SFML.h
  imgui-SFML_export.h
  imgui.h
  imgui_internal.h
  imstb_rectpack.h
  imstb_textedit.h
  imstb_truetype.h
  DESTINATION include
  )
# Rule to install the source -> Usually this is not necessary, but since imgui
# uses the source as documentation we also install the source in the conan cache
install(FILES
  imgui-SFML.cpp
  imgui.cpp
  imgui_demo.cpp
  imgui_draw.cpp
  imgui_tables.cpp
  imgui_widgets.cpp
  DESTINATION src
  )
