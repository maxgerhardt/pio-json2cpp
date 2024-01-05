Import("env")
from pathlib import Path
from platformio import util
import os
import sys
import urllib.request
import zipfile
import tarfile

json2cpp_download_url = {
    # Windows
    "windows_amd64": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Windows-Release-Clang-15.0.2.tar.bz2",
    "windows_x86": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Windows-Release-Clang-15.0.2.tar.bz2",
    # No Windows ARM64 or ARM32 builds.
    # Linux
    "linux_x86_64": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Linux-Release-Clang-15.0.2.tar.bz2",
    "linux_i686": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Linux-Release-Clang-15.0.2.tar.bz2",
    # No Linux ARM (linux_aarch64, linux_armv7l, linux_armv6l)
    # Mac (Intel and ARM use same)
    "darwin_x86_64": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Darwin-Release-Clang-15.0.2.tar.bz2",
    "darwin_arm64": "https://github.com/lefticus/json2cpp/releases/download/snapshot-fc69acfd190ff0aa23689fae339ed89db4c3ed75/json2cpp-0.0.1-fc69acfd-Darwin-Release-Clang-15.0.2.tar.bz2"
}

PROJ_DIR = Path(env.subst("$PROJECT_DIR"))
JSON2CPP_PATH = PROJ_DIR / "json2cpp"
JSON_INPUT_DIR = PROJ_DIR / "json_files"
JSON_CPP_OUTPUT_DIR = PROJ_DIR / "src" / "genned_json"
JSON2CPP_BINARY = JSON2CPP_PATH / "bin" / ("json2cpp" + (".exe" if "windows" in util.get_systype() else ""))

def download_json2cpp_if_not_present():
    # Download not needed
    #print("Checking path " + str(JSON2CPP_PATH))
    if os.path.isdir(str(JSON2CPP_PATH)):
        return
    # get system type
    sys_type = util.get_systype()
    if sys_type not in json2cpp_download_url:
        sys.stderr.write("No precompiled package for system type %s\n" % sys_type)
        env.Exit()
    # download
    url = json2cpp_download_url[sys_type]
    print("Downloading json2cpp from %s" % url)
    (file, httpresp) = urllib.request.urlretrieve(url)
    if url.endswith(".zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(JSON2CPP_PATH)
            print("Extracted ZIP file.")
    elif url.endswith(".tar.bz2"):
        tar = tarfile.open(file, "r:bz2")  
        tar.extractall(JSON2CPP_PATH)
        tar.close()
    # will now have something like json2cpp/json2cpp-0.0.1-fc69acfd-Windows-Release-MSVC-19.34.31944.0/{bin, include, share}
    # move everything one up
    subfolder = None
    for subfolder in JSON2CPP_PATH.iterdir():
        for file in subfolder.iterdir():
            file.rename(JSON2CPP_PATH / file.name)
    # cleanup empty folder
    subfolder.rmdir()

def generate_files_from_json():
    if not JSON_CPP_OUTPUT_DIR.is_dir():
        JSON_CPP_OUTPUT_DIR.mkdir()
    for json_file in JSON_INPUT_DIR.iterdir():
        if not json_file.is_file():
            continue
        # invoke the tool
        document_name = json_file.stem + "_json"
        output_base = JSON_CPP_OUTPUT_DIR / document_name
        env.Execute(" ".join([
            '"%s"' % str(JSON2CPP_BINARY),
            '"%s"' % document_name,
            '"%s"' % str(json_file),
            '"%s"' % str(output_base),
        ]))

# check this on every script invoke
download_json2cpp_if_not_present()

# Add to include path in any case
env.Append(CPPPATH=[str(JSON2CPP_PATH / "include")])

# generate cpp files from JSON before compilation begins now.
# this happens on each script invoke.
# Could use SCons system to only do this if change in dependency (.json file) is detected, good for now.
generate_files_from_json()