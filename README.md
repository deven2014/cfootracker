# Cfootracker V2.0
Cfootracker is a light debug enhance tool for C++ system. 
- By using it one can get function trace records of the system at any time, 
  in a efficient way and almost no lost of any performance of the system. 
- The tool supports one file, multiple files/path so it is easy to limit the 
  scope of the affected files. (suppose uses know where they want to deep in) 
- Technically the tool add a statistics function to the system and insert 
  trace record for each function(foo) belongs to the input source files. 

How to use

- No need to install. Just need python3 runtime environment and g++.
- "cfootrack.py" is the only program to run the tool.
- "footracker.cpp" is a reference code which need to be copied to one or 
  several files in the source code of the target system.

Steps for copy c++ codes

1. Select the main.cpp or the source file which holds the top level function
   of the program as the file in which the FoolTracker class implement.
2. The definition together with the implementation of the class FooTracker 
   should be copied from the source file "footracker.cpp". 
3. No head file needs to be included for simplify the config.
4. The main function or 'top level function' should have the possiblility 
   to use std::cout for debug info for function tracking info.
5. The main function or 'top level function' should have the possiblility 
   to use std::ofstream for dump tracking info to file.
6. In where to call dump interface depends on the practical situation.
7. It is better to run the command in a independent dir.

   test/main.cpp is an example for you to pratice this tool.

General commands for using the tool (based on the test/main.cpp)

 ../cfootrack.py full path ./   [add track code in .cpp files in ./ dir]
 make app                       [compile target system]
 ./app                          [run target system] 
 vi filter                      [prepare a filter file for parsing]
 ../cfootrack.py parse filter   [parse the statistics result]
 cat footrackstat.dat.result    [show the parsed result]
 ../cfootrack.py restore path   [restore the source files]
 ../cfootrack.py clear all      [clear the temporary files of this task]


Feature list:

* : Done | S : Scheduled, ongoing | - : Not support 

Target Scope Control

* Add function trace for one file
* Add function trace for all ".cpp" files in one path 
S Add function trace for all files defined in a "list" file 
S Support an "ignored" file to ignored files as input files
- Config the program for make target scope into "function" granularity. 
* 

Performance

* Support max 10000 statistics records which occupies about 80K memory.
- Support config of the max numbers of statistics record.
* Very small cpu resource comsuption. (suitable for time critical system)
- Interface defined as inline function for best performance.

Statistics Result
- Support specify the output file and path

Parse Statistics Result

* Support parse the statistics result to (function, file, line) records.
- Customize the parsed result format. (show less items for example)  
* Support filter file which can define some functions. The parsed result will
  not include records match these functions. (Easiler to read the result) 

Analyze result

- From trace record jump to (file,line) directly in VIM.

Restore

* Support restore the source files of the project.
* Clear command to erase all temporary files.

Help

- Completely help document also support --help parameter.
