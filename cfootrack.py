#!/usr/bin/env python3
#                                                                             E
import sys, os
from shutil import copyfile

"""
Author: Liang Deng
Date: 2018-11-27
Version: 2.0
Revesion history:
2018-11-27, initiated version. v0.1
2018-12-10, corrected the case when '{' in second line of functions definition.
            v0.2
2018-12-11, added index number in each function track point to make 
            troubleshooting easier. v0.3
2019-06-14, Enhance program. V2 provides statistics info of function trace and 
            parser the log offline. It supports for whole system function trace.

"""
class SourceAnalysisV1:
    m_fn = '' # file name which stores the source file
    m_fpath = '' # file path of the source file, includes file name
    m_cxx_statement_keys = ['if', 'while', 'for', 'switch', 'try', 
            'namespace', 'using', 'catch', '&&', '||']
    m_trackpoint_index = 0

    def __init__(self, path, type = 'CXX'):
        """
        - default type is CXX which means C/C++
        - further type may be added in the furture
        """
        self.m_fpath = path
        self.m_fn = self.extract_file_name(path)
        print(self.__str__())

    def __str__(self):
        return('Source Analysis class V0.1. \nAuthor Liang Deng 2018.11.')

    def extract_file_name(self, path):
        return path.split('/')[-1]

    def replace_file_name(self, path, fn):
        path_tmp = path.split('/')[:-1]
        # Current dir
        if(not len(path_tmp)):
            path_tmp = '.'
        return '/'.join(path_tmp) + '/' + fn

    def insert_foo_track(self, pattern = 'FUNC() enter.'):
        """
        insert function tracks to the source file. 
        - pattern can specify what string should be added to source code, 
          'FUNC' is key word and will be replace by the real function name.
        - if a line end with ')' then this function checks if the next line is 
          only only '{'. If so it will merge the second line to the end of 
          first line before processing it. 
        """
        print('Start to insert function tracks to the source file...')
        first_line_s = ''
        with open(self.m_fpath, 'r') as fi:
            print('Input file: ', self.m_fn)
            print('Input file path: ', self.m_fpath)
            o_fn = sys.argv[3] if len(sys.argv)>3 else 'out_'+self.m_fn
            o_fpath = self.replace_file_name(self.m_fpath, o_fn)
            print('Ouput file: ', o_fn)
            print('Ouput file path: ', o_fpath)
            print('found these functions:')
            print('======================')
            with open(o_fpath, 'w') as fo:
                for line in fi:
                    stripped_line = line.strip()
                    if first_line_s:
                        if stripped_line == '{':
                            #print('Merge line:', first_line_s, stripped_line)
                            line = first_line_s + line 
                            first_line_s = ''
                        else:
                            #print('copy first line to new file')
                            fo.write(first_line_s)
                            first_line_s = ''

                    if(len(stripped_line) and stripped_line[-1]==')'):
                        first_line_s = line
                        #print('set first line:', first_line_s)
                        continue

                    fo.write(line)
                    (ret, foo_name) = self.is_cxx_foo(line)
                    if ret:
                        #track info template "footrack(file,foo:index): foo()"
                        fo.write('    std::cout << "footrack(' + self.m_fn + 
                                ',' + str(self.m_trackpoint_index) + 
                                '): ' + foo_name + 
                                ' enter." << std::endl;\n')
                        self.m_trackpoint_index += 1
            fo.close()
        fi.close()

    def convertline(self, si):
        return(si) 
    
    def is_cxx_foo(self, s):
        """
        - true, return (1, foo_name)
        - false, return (0, '')
        """
        words = s.strip().split()
        ret = 0
        foo_name = ''
        
        # void foo(){
        if len(words) < 2:
            return (ret, foo_name) 

        # Only aware multiple lines function currently
        # foo(...){ or foo(...) { 
        if words[-1] != '{' and words[-1][-1] != '{':
            return (ret, foo_name) 

        # () have to present. - skip () in two rows case since it is too 
        # complex
        if ((not '(' in s) or (not ')' in s)):
            return (ret, foo_name)

        if words[0] in self.m_cxx_statement_keys:
            return (ret, foo_name) 

        # Assume the string is one function statement
        foo_name = words[1]
        
        # If foo name without ( should be not foo 
        if ('(' not in foo_name):
            return (ret, '')

        # Omit the real arguments. 
        foo_name = foo_name.split('(')[0] + '()'

        print(foo_name) 
        ret = 1
        return (ret, foo_name) 

# Global configuration.

# These extern interface statements will be added to the beginning of cpp files 
EXTERN_INTERFACE_STATEMENTS = ['extern void fooTrackerLog(long long int index);']

# Code pattern for statistics. for example 'fooTracker->log(1001);'
STAT_CODE_PATTERN = {
        'code_fixed_statement': 'fooTrackerLog',
        'code_end': ';'
        }

# Excluded files. These files will be skipped for add on code.
EXCLUDED_FILE_LIST = []

# Excluded dirs. These dirs will be skipped for add on code.
EXCLUDED_PATH_LIST = []

# Excluded filter. An regular expression for excluding files or dirs.
EXCLUDED_FILTER = ''

# Excluded functions. These function will be skipped for add on code.
EXCLUDED_FUNCTION_LIST = [ 'main', 
                           'FooTracker::log', 
                           'FooTracker::dump2file', 
                           'FooTracker::dump', 
                           'fooTrackerLog', 
                           'initFooTracker', 
                           'dumpFooTrackInfo' ]

# Add on key words for exclude none-function definition statements.
# The basic cxx statement keys has been added as default config
ADD_ON_EXCLUDED_KEYWORD_LIST = []

# File name of dumped trackpoint info 
DEFAULT_DUMP_TRACKPOINT_INFO_FILE = './trackpoint.info'

# File name of save the program run result 
DEFAULT_RESULT_FILE = './run.result'

# File name of run log, import for restore transaction. 
DEFAULT_RUN_LOG_FILE = './run.log'

# File name of stat data, this file is generated by the application. 
DEFAULT_STAT_DATA_FILE = './footrackstat.dat'

class SourceAnalysisV2:
    """
    SourceAnalysisV2 can insert statistics code to source code whih predefined patterns.
    """
    cxx_statement_keys = ['if', 'while', 'for', 'switch', 'try', 
            'namespace', 'using', 'catch', '&&', '||']

    def __init__(self, op_type, path, language_type = 'CXX'):
        """
        - default type is CXX which means C/C++
        - further type may be added in the furture
        """
        # up to 64 bit integer which can store almost unlimited trace points 
        self.trackpoint_index = 0

        # Each item in this list stores the information for this track point.
        # The stucture of the item is ['file_path, line, foo_name', ...]
        self.trackpoint_info_list = [] 
        self.source_file_path = '' # file path of the source file, includes file name
        self.source_file_name = '' # file name which stores the source file
        self.source_path = ''      # dir path of the source files
        self.dest_file_path = ''   # file path of the output file, includes file name

        self.operation_mode = op_type # FILE | PATH 
        if op_type == 'FILE':
            self.source_file_name = self.extract_file_name(path)
            self.source_file_path = path

            # dest file name is same as source file name (replace)
            self.dest_file_path = self.source_file_path
            #fn = 'out_' + self.source_file_name
            #self.dest_file_path = self.replace_file_name(self.source_file_path, fn)
        elif op_type == 'PATH':
            self.source_path = path
        elif op_type == 'RESTORE_FILE' or op_type == 'RESTORE_PATH':
            self.restore_transaction()
        elif op_type == 'PARSE':
            # The path is a filter file which excludes some log to be shown
            self.parse_stat_data(path)

        print(self.__str__())

    def __str__(self):
        return('Source Analysis class V2.0.')

    def extract_file_name(self, path):
        return path.split('/')[-1]

    def replace_file_name(self, path, fn):
        path_tmp = path.split('/')[:-1]
        # Current dir
        if(not len(path_tmp)):
            path_tmp = '.'
        return '/'.join(path_tmp) + '/' + fn

    def get_source_file_list(self, path):
        flist = []
        for fpath, dirs, fs in os.walk(path):
            for f in fs:
                # Only take cpp files
                ext = os.path.splitext(f)[1]
                if ext == '.cpp' or ext == '.CPP' or ext == '.Cpp':
                    flist.append(os.path.join(fpath, f))
        return flist
  
    def insert_foo_track(self):
        # Insert function track statistics code to the source file(s). 

        # Clear last time run log
        self.clear_run_log()

        if self.operation_mode == 'FILE':
            self.insert_file_foo_track()
            return

        # PATH mode
        print('Start to insert function tracks to the path:')
        print(self.source_path)

        # TODO: excluded path, file, filter should be added
        # Get a list of source files then one by one process
        source_file_list = self.get_source_file_list(self.source_path)

        print('Total', len(source_file_list), 'files need to be processed.')
        for file_path in source_file_list:
            self.source_file_name = self.extract_file_name(file_path)
            self.source_file_path = file_path
            # dest file name is same as source file name (replace)
            self.dest_file_path = self.source_file_path
            self.insert_file_foo_track()

        print('Done.')
        

    def insert_file_foo_track(self):
        """
        insert function track statistics code to the source file. 
        - Program scans all cxx file(s), if a line end with '){' (after 
          removing spaces) or if a line end with ')' and next line is only '{', 
          this line may be a function body. the statistics code will be added 
          at the beginning of the function block. 
          If that is a two-line case the program will merge the second line '{'
          to the end of first line before judging if it is a function block. 
        """
        # Backup the source file to be able to restore the file to origin
        # TODO: check the exception
        # print(self.source_file_path)
        copyfile(self.source_file_path, self.source_file_path + '.backup')

        # Set backup file as source file since the real source file will be changed
        self.source_file_path = self.source_file_path + '.backup'

        first_line_s = ''
        # Extern statements should be added right after the include statements.
        extern_statement_added = False

        with open(self.source_file_path, 'r') as fi:

            # For one file mode show detail result info for one file
            if self.operation_mode == 'FILE':
                print('Input file: ', self.source_file_name)
                print('Input file path: ', self.source_file_path)
                print('Ouput file: ', self.extract_file_name(self.dest_file_path))
                print('Ouput file path: ', self.dest_file_path)
                print('found these functions:')
                print('======================')
            else:
                print('Processing file: ', self.source_file_name)

            line_no = 1
            with open(self.dest_file_path, 'w') as fo:

                # Write a run log for restore
                self.write_run_log(self.source_file_path)

                for line in fi:
                    stripped_line = line.strip()

                    # Extern statements should be added right after the include statements.
                    if(not self.is_include_statement(stripped_line) and 
                            not extern_statement_added):
                        fo.write('\n'.join(EXTERN_INTERFACE_STATEMENTS) + '\n')
                        extern_statement_added = True

                    if first_line_s:
                        if stripped_line == '{':
                            line = first_line_s + line 
                            first_line_s = ''
                        else:
                            fo.write(first_line_s)
                            first_line_s = ''

                    if(len(stripped_line) and stripped_line[-1]==')'):
                        first_line_s = line
                        continue

                    fo.write(line)
                    line_no += 1

                    (ret, foo_name) = self.is_cxx_foo(line)
                    if ret:
                        # Insert code pattern for statistics. for example 'fooTracker->log(1001);'
                        fo.write('    ' + STAT_CODE_PATTERN['code_fixed_statement'] + 
                                 '(' + str(self.trackpoint_index) + ')' + 
                                 STAT_CODE_PATTERN['code_end'] + '\n')

                        # Store the statisctics point info
                        self.trackpoint_info_list.append(
                                foo_name + ', ' +
                                self.dest_file_path + ', ' +
                                str(line_no))

                        line_no += 1
                        self.trackpoint_index += 1
            fo.close()
        fi.close()

    def convertline(self, si):
        return(si) 
    
    def dump_trackpoint_info(self):
        with open(DEFAULT_DUMP_TRACKPOINT_INFO_FILE, 'w') as fi:
            fi.write('\n'.join(self.trackpoint_info_list))
            print("Dump track point infomation to file:")
            print(DEFAULT_DUMP_TRACKPOINT_INFO_FILE)
            print('Done.')

    def clear_run_log(self):
        with open(DEFAULT_RUN_LOG_FILE, 'w') as fi:
            fi.write('')

    def write_run_log(self, log):
        with open(DEFAULT_RUN_LOG_FILE, 'a') as fi:
            fi.write(log+'\n')

    def restore_transaction(self):
        with open(DEFAULT_RUN_LOG_FILE, 'r') as fi:
            for line in fi:
                # From .backup file to origin file
                # TODO: exception process 
                file_path = line.strip('\n')
                copyfile(file_path, file_path[:-7])

                #delete the backup file
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    print('Error:%s file not found' % file_path)

        self.clear_run_log()
        print('Restore last transaction done.')

    def parse_stat_data(self, filter_file_name = ''):
        foo_tracker_result = []
        data_list = []
        traceinfo_list = []
        filter_list = []
        data_file_name = DEFAULT_STAT_DATA_FILE

        with open(data_file_name, 'r') as fi:
            # 0 1 2 12
            data_list = fi.read().split()

        with open(DEFAULT_DUMP_TRACKPOINT_INFO_FILE, 'r') as ftraceinfo:
            traceinfo_list = ftraceinfo.read().split('\n')

        if filter_file_name:
            with open(filter_file_name, 'r') as ffilter:
                filter_list = ffilter.read().split('\n')

        maximum_index = len(traceinfo_list)
        for item in data_list:
            index_value = int(item)
            if index_value < len(traceinfo_list):
                trace_info = traceinfo_list[index_value]
            else:
                trace_info = 'Unknown function()!'
            filter_flag = self.check_result_filter(trace_info, filter_list) 
            # print(index_value, maximum_index, filter_flag)
            if index_value < maximum_index and not filter_flag:
                foo_tracker_result.append(trace_info)

        with open(DEFAULT_STAT_DATA_FILE + '.result', 'w') as ftraceresult:
            ftraceresult.write('\n'.join(foo_tracker_result))

    def check_result_filter(self, log, filter_list):
        # Check if log includes any name in filter_list 
        for item in filter_list:
            # Empty filter should not be used 
            if item and (item in log):
                return True
        return False

    def is_cxx_foo(self, s):
        """
        - true, return (1, foo_name)
        - false, return (0, '')
        """
        words = s.strip().split()
        ret = 0
        foo_name = ''
        
        # void foo(){
        if len(words) < 2:
            return (ret, foo_name) 

        # Only aware multiple lines function currently
        # foo(...){ or foo(...) { 
        if words[-1] != '{' and words[-1][-1] != '{':
            return (ret, foo_name) 

        # () have to present. - skip () in two rows case since it is too 
        # complex
        if ((not '(' in s) or (not ')' in s)):
            return (ret, foo_name)

        if words[0] in self.cxx_statement_keys:
            return (ret, foo_name) 

        # Assume the string is one function statement
        foo_name = words[1]
        
        # If foo name without ( should be not foo 
        if ('(' not in foo_name):
            return (ret, '')

        # Omit the real arguments. 
        foo_name = foo_name.split('(')[0] + '()'

        # Omit the excluded functions
        if foo_name[:-2] in EXCLUDED_FUNCTION_LIST:
            return (0, '')

        # print(foo_name) 
        ret = 1
        return (ret, foo_name) 

    def is_include_statement(self, s):
        return (s[:8] == '#include')

    @staticmethod
    def clear_temporary_files(cmd):
        # List of temporary files
        # TODO: since the file name is configrable in the furture, should get 
        #       correct file names from member variables instead of hard code
        file_list = ['footrackstat.dat', 'footrackstat.dat.result', 'run.log', 'trackpoint.info']
        
        #delete the temporary files
        for file_path in file_list:
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                print('Error:%s file not found' % file_path)
        print('Clear', cmd, 'Done.')

def show_command_help():
    print('command parameters option:')
    print(' 1. simple <source file name>')
    print(' 2. full file <source file name>')
    print(' 3. full path <source file dir>')
    print(' 4. parser <trace data file path>')
    print(' 5. restore file')
    print(' 6. restore path')
    print(' 7. parse <filter file path>')
    print(' 8. config list')
    print(' 9. config <parameter name> <parameter value>')
    print('10. clear all')

if __name__ == '__main__':
    #print("run cmd with argc: ", len(sys.argv))
    #for cmd in sys.argv:
    #    print(cmd)

    if(len(sys.argv) < 3):
        show_command_help()
        exit(1)

    op_type = sys.argv[1]
    if(op_type == 'simple'):
        print('Simple mode, add on foo track log info for one file.')
        sa = SourceAnalysisV1(sys.argv[2])
        sa.insert_foo_track()
    elif(op_type == 'full'):
        op_sub_type = sys.argv[2]
        if op_sub_type == 'file':
            print('Full mode, add on foo track statistics info for one source files.')
            sa = SourceAnalysisV2('FILE', sys.argv[3])
            sa.insert_foo_track()
            sa.dump_trackpoint_info()
        elif op_sub_type == 'path':
            print('Full mode, add on foo track statistics info for all source files.')
            sa = SourceAnalysisV2('PATH', sys.argv[3])
            sa.insert_foo_track()
            sa.dump_trackpoint_info()
        else:
            print('Wrong papameter imput.')
            show_command_help()
    elif(op_type == 'restore'):
        op_sub_type = sys.argv[2]
        if op_sub_type == 'file':
            print('restore the original file of last run.')
            sa = SourceAnalysisV2('RESTORE_FILE', '') 
        elif op_sub_type == 'path':
            print('restore the original files of last run.')
            sa = SourceAnalysisV2('RESTORE_PATH', '') 
        else:
            print('Wrong papameter imput.')
            show_command_help()
    elif(op_type == 'parse'):
        print('parse a stat data.')
        sa = SourceAnalysisV2('PARSE', sys.argv[2]) 
        sa.parse_stat_data(sys.argv[2])
    elif(op_type == 'config'):
        print('config')
    elif(op_type == 'clear'):
        print('Clear the temporary files ...')
        SourceAnalysisV2.clear_temporary_files(sys.argv[2]);
    else:
        print('Wrong papameter imput.')
        show_command_help()
        exit(1)
