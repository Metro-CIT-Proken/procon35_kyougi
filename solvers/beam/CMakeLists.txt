cmake_minimum_required(VERSION 3.22)
project(solver CXX)
enable_testing()

add_subdirectory(libs/json)
add_subdirectory(libs/acutest)

add_executable(solver src/main.cpp src/board.cpp)
target_link_libraries(solver PRIVATE nlohmann_json::nlohmann_json)

add_executable(test_board test/test_board.cpp src/board.cpp)
include_directories(libs/acutest/include)
target_link_libraries(test_board PRIVATE nlohmann_json::nlohmann_json)
add_test(NAME test_board COMMAND test_board)