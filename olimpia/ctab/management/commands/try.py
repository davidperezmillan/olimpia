#!/usr/bin/env python
from datetime import datetime
        
if __name__ == "__main__":
    
    
    import shlex
    argString = '-vvvv -c "yes, Podemos" --foo bar --some_flag'
    args = shlex.split(argString)
    print args
        
