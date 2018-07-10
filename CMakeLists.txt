cmake_minimum_required(VERSION 3.10)
project(imgui-sfml)

# PLACEHOLDER

find_package(SFML REQUIRED COMPONENTS system window graphics network audio)

add_library(imgui-sfml
  imconfig.h
  imgui.cpp
  imgui_demo.cpp
  imgui_draw.cpp
  imgui.h
  imgui_internal.h
  imgui-SFML.cpp
  imgui-SFML.h
  stb_rect_pack.h
  stb_textedit.h
  stb_truetype.h
  )

target_include_directories(imgui-sfml SYSTEM PUBLIC .)
target_link_libraries(imgui-sfml PUBLIC sfml-graphics sfml-window sfml-system sfml-network sfml-audio)
target_link_libraries(imgui-sfml PUBLIC "-lGL")


install(TARGETS imgui-sfml DESTINATION lib)
install(FILES
  imconfig.h
  imgui.h
  imgui_internal.h
  imgui-SFML.h
  stb_rect_pack.h
  stb_textedit.h
  stb_truetype.h
  DESTINATION include
  )
