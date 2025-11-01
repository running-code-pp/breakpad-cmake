# why create this repository?
I planned to integrate Breakpad via Conan, but discovered it wouldn't build on Windows. Therefore, I cloned the Breakpad 2024.02.16 source code and created a CMake build script for it. You can now add it to your local Conan repository and build it using CMake.

# how to use it through conan

## Method 1: Add to Local Conan Cache

### Step 1: Export the recipe to your local Conan cache

```bash
# In the project root directory
conan export . --user=your_user --channel=stable
```

Or simply:
```bash
conan export .
```

This will add the package recipe to your local Conan cache as `breakpad/2024.02.16`.

### Step 2: Use it in your project

Add to your project's `conanfile.txt`:
```ini
[requires]
breakpad/2024.02.16

[generators]
CMakeDeps
CMakeToolchain

[options]
breakpad:build_processor=True
breakpad:build_client=True
breakpad:build_tools=False
```

Or in your `conanfile.py`:
```python
from conan import ConanFile

class YourProjectConan(ConanFile):
    requires = "breakpad/2024.02.16"
    
    def configure(self):
        self.options["breakpad"].build_processor = True
        self.options["breakpad"].build_client = True
        self.options["breakpad"].build_tools = False
```

### Step 3: Install dependencies

```bash
conan install . --output-folder=build --build=missing
```

### Step 4: Build your project with CMake

```bash
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build .
```

## Method 2: Create Local Conan Package

If you want to build and cache the binaries:

```bash
# Create the package in local cache
conan create . --build=missing

# Or with specific options
conan create . --build=missing -o build_processor=True -o build_client=True -o build_tools=False
```

## Method 3: Use Editable Mode (For Development)

If you're actively developing or modifying the breakpad package:

```bash
# Add as editable package
conan editable add . breakpad/2024.02.16

# Your changes will be immediately reflected in dependent projects
# When done, remove editable mode:
conan editable remove breakpad/2024.02.16
```

## Available Options

- `shared`: Build shared libraries (default: False)
- `fPIC`: Build with position independent code (default: True, not available on Windows)
- `build_processor`: Build breakpad processor library (default: True)
- `build_client`: Build breakpad client library (default: True)
- `build_tools`: Build breakpad tools (default: False)

## Example: Using in CMakeLists.txt

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
