import subprocess

###############
## __LINUX___##
###############

# Git, Python, node.js, CMake, and Java are not provided by emsdk. The user is expected to install these beforehand with the system package manager:

# # Install git
"""sudo apt-get install git-core"""
# # Install Python
"""sudo apt-get install python2.7"""
# # Install node.js
"""sudo apt-get install nodejs"""
# # Install CMake (optional, only needed for tests and building Binaryen)
"""sudo apt-get install cmake"""
# # Install Java (optional, only needed for Closure Compiler minification)
"""sudo apt-get install default-jre"""


print("")
print("******************************************************************")
print("*  It May take multiple minuts to install all requiret software  *")
print("******************************************************************\n\n")
# subprocess.call(['./install.sh'])

