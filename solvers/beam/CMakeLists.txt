cmake_minimum_required(VERSION 3.22)
project(solver CXX)
enable_testing()

option(CPU_ARM "solver will be compiled ARM arch." OFF)

if(CPU_ARM)
    set(CMAKE_CXX_STANDARD 23)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++23 -O3")
    message("ARM")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mbmi2 -mbmi -mabm -std=c++23 -O3")
    message("x86")
endif()

# TBB
find_package(TBB REQUIRED)
message(STATUS "Found 'TBB library' ${TBB_VERSION} ${TBB_LIBRARIES}")

add_subdirectory(libs/json)
add_subdirectory(libs/acutest)
include_directories(libs/acutest/include)
include_directories(libs/bitarray)

add_executable(solver 
    src/main.cpp 
    src/board.cpp 
    src/BeamSolver.cpp
    # src/BeamSolver_chokudai.cpp
    src/bitboard.cpp 
    src/VDivideSolver.cpp
    src/LineCountSolver.cpp
    src/BeamEvaluator.cpp
)
target_link_libraries(solver PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(solver PRIVATE TBB::tbb)

add_executable(solver_simple
    src/main_SimpleSolver.cpp
    src/board.cpp
    src/SimpleSolver.cpp
)
target_link_libraries(solver_simple PRIVATE nlohmann_json::nlohmann_json)

# tests
add_executable(test_board test/test_board.cpp src/board.cpp)
target_link_libraries(test_board PRIVATE nlohmann_json::nlohmann_json)
add_test(NAME test_board COMMAND test_board)

# add_executable(test_bitboard test/test_bitboard.cpp src/board.cpp src/bitboard.cpp)
# target_link_libraries(test_bitboard PRIVATE nlohmann_json::nlohmann_json)
# add_test(NAME test_bitboard COMMAND test_bitboard)

# add_executable(test_LineCountSolver test/test_LineCountSolver.cpp src/LineCountSolver.cpp src/board.cpp src/bitboard.cpp)
# target_link_libraries(test_LineCountSolver PRIVATE nlohmann_json::nlohmann_json)
# add_test(NAME test_LineCountSolver COMMAND test_LineCountSolver)
