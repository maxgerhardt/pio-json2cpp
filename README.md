# PlatformIO + json2cpp

## Description

Uses https://github.com/lefticus/json2cpp to convert the files in [json_files](json_files) to `.cpp` and `.hpp` files that can be directly included in the code.

It first downloads a snapshot of json2cpp to the `json2cpp` folder, then invokes the `json2cpp` binary on each file in `json_files`, writing the output to `src/genned_json/*`. These files will be compiled and referenced in `src/main.cpp`

Various settings can be changed inside the `use_json2cpp.py` file. 

To use this inside another project:
1. Copy over `use_json2cpp.py` to the root of your project
2. Reference it with `extra_scripts = pre:use_json2cpp.py`
3. Adapt settings such as JSON source folder, output folder, etc., in script
4. Make sure the project uses the C++17 standard or higher, otherwise compilation will fail. Use `build_flags` and `build_unflags` as needed

This repo contains a ESP32 firmware that should output on the monitor:

```
JSON doc size: 4  
Elements in array:
10.00
20.00
30.00
40.00
```