#!/usr/bin/env python
"""
shotgun.py 

Copyright (c) 2010 Andre LeBlanc

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import time
import subprocess
import sys
from optparse import OptionParser
import fileinput


def mkproc(shellcmd):    
    """Create and return a subprocess ready to recieve input on stdin"""
    return subprocess.Popen([shellcmd], 
                             shell=True, 
                             stdin=subprocess.PIPE,                          
                             stdout=sys.stdout,
                             close_fds=True)
    


parser = OptionParser(usage="""usage: %prog [OPTION]... [FILE]...

spawns multiple subprocesses and maps input lines to them.""", version="%prog 0.1a")

parser.add_option("-p", "--processes", action='store', type='int', default=2,help="The number of subprocesses to run")
parser.add_option("-c", "--command", action='store', default='cat', help="the command-line to execute for each subprocess.")

if __name__ == '__main__':
    options, args = parser.parse_args()

    # Create a pool of subprocesses to handle the incoming lines.
    pool = [mkproc(options.command) for x in range(options.processes)]

    # "deal out" the input lines to the subprocesses in the pool.
    for i,line in enumerate(fileinput.input(args)):
        pool[i % options.processes].stdin.write(line)
            
    # Close stdin on the processes. lets the other end get an EOF.
    for proc in pool:
        proc.stdin.close()

    # Wait for all subprocesses to finish their work before exiting.
    for proc in pool:
        proc.wait()
                    