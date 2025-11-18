# why create this repository?
I planned to integrate Breakpad via Conan, but discovered it wouldn't build on Windows. Therefore, I cloned the Breakpad 2024.02.16 source code and created a CMake build script for it. You can now add it to your local Conan repository and build it using CMake,the breakpad package in conan center can just use in liux

# Install as local conan packages

To install this Breakpad package to your local Conan package repository:

1. First, ensure you have Conan installed and configured:
   ```bash
   conan --version
   conan profile detect --force
   ```

2. Export the package recipe to your local cache:
   ```bash
   # Navigate to the project root directory
   cd d:/third_libs/breakpad-cmake
   
   # Export the recipe
   conan export .
   ```

3. Build and install the package with specific options:
   ```bash
   # Create and install the package with default options
   conan create . --build=missing
   
   # Or create with specific options
   conan create . --build=missing -o breakpad/*:build_processor=True -o breakpad/*:build_client=True -o breakpad/*:build_tools=False
   ```

4. Verify the package installation:
   ```bash
   conan list breakpad/2024.02.16
   ```

5. The package is now available for use in other projects with:
   ```ini
   [requires]
   breakpad/2024.02.16
   ```


# Example: Using in CMakeLists.txt

After installing dependencies with Conan, you can link against Breakpad in your CMake project:

```cmake
cmake_minimum_required(VERSION 3.15)
project(MyProject)

# Find the package
find_package(breakpad REQUIRED)

# Link against client library
add_executable(my_app main.cpp)
target_link_libraries(my_app breakpad::client)

# Or link against processor library
add_executable(my_processor processor.cpp)
target_link_libraries(my_processor breakpad::processor)
```