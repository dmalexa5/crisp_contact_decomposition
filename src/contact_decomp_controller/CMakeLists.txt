cmake_minimum_required(VERSION 3.16)
project(contact_decomp_controller)

find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
  message(STATUS "Using ccache")
  set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
  set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
endif()


# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

# Enable precompiled headers
option(USE_PRECOMPILED_HEADERS "Use precompiled headers" ON)

option(CHECK_TIDY "Adds clang-tidy tests" OFF)

option(ENABLE_NATIVE_OPTIMIZATION
  "Enable CPU-specific optimizations (-march=native)"
  OFF
)

# Default to release build
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Compiler flags by build type
add_library(project_compile_options INTERFACE)
target_compile_options(project_compile_options INTERFACE
  # Warnings (build only)
  $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>

  # Debug
  $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang>>:-O0 -g>

  # Release
  $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:GNU,Clang>>:-O3 -DNDEBUG>
)

# Optional CPU-specific optimizations (non-portable)
if(ENABLE_NATIVE_OPTIMIZATION)
  target_compile_options(project_compile_options INTERFACE
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:GNU,Clang>>:-march=native>
)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(controller_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(pinocchio REQUIRED)
find_package(realtime_tools REQUIRED)
find_package(generate_parameter_library REQUIRED)

generate_parameter_library(
  contact_decomp_controller_parameters
  src/contact_decomp_controller.yaml
)

add_library(
  ${PROJECT_NAME}
  SHARED
  src/contact_decomp_controller.cpp
)

target_link_libraries(${PROJECT_NAME}
  PRIVATE
    project_compile_options
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

if(USE_PRECOMPILED_HEADERS)
    target_precompile_headers(${PROJECT_NAME} 
        PRIVATE
        include/contact_decomp_controller/pch.hpp
    )
endif()

# Link parameter libraries to the main library
target_link_libraries(${PROJECT_NAME}
  PRIVATE
    contact_decomp_controller_parameters
)


ament_target_dependencies(${PROJECT_NAME}
  PUBLIC
    controller_interface
    hardware_interface
    pluginlib
    rclcpp
    rclcpp_lifecycle
    pinocchio
    generate_parameter_library
    realtime_tools
    rsl
    tl_expected
)

pluginlib_export_plugin_description_file(
        controller_interface contact_decomp_controller.xml)

install(
        TARGETS
        ${PROJECT_NAME}
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
)

install(
        DIRECTORY include/
        DESTINATION include
)

ament_export_include_directories(
        include
)
ament_export_libraries(
        ${PROJECT_NAME}
)
ament_export_dependencies(
  controller_interface
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
  pinocchio
  generate_parameter_library
  realtime_tools
  rsl
  tl_expected
)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  ament_add_gtest(test_contact_decomp_controller
    tests/test_contact_decomp_controller.cpp
  )
  target_link_libraries(test_contact_decomp_controller
    Eigen3::Eigen
    ${PROJECT_NAME}
  )
endif()

ament_package()