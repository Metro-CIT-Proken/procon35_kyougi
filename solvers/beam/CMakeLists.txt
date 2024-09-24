cmake_minimum_required(VERSION 3.22)
project(solver CXX)
enable_testing()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mbmi2 -mbmi -mabm -std=c++23 -O3 -save-temps")

add_subdirectory(libs/json)
add_subdirectory(libs/acutest)
include_directories(libs/acutest/include)
include_directories(libs/bitarray)

add_executable(solver 
    src/main.cpp 
    src/board.cpp 
    src/BeamSolver.cpp
    src/BeamSolver_chokudai.cpp
    src/bitboard.cpp 
    src/VDivideSolver.cpp)
target_link_libraries(solver PRIVATE nlohmann_json::nlohmann_json)

# tests
add_executable(test_board test/test_board.cpp src/board.cpp)
target_link_libraries(test_board PRIVATE nlohmann_json::nlohmann_json)
add_test(NAME test_board COMMAND test_board)

add_executable(test_bitboard test/test_bitboard.cpp src/board.cpp src/bitboard.cpp)
target_link_libraries(test_bitboard PRIVATE nlohmann_json::nlohmann_json)
add_test(NAME test_bitboard COMMAND test_bitboard)