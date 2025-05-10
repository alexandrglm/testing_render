############################################################################
# REACT SELF-DEPLOYMENTS
#############
import os
import subprocess

#############
# Project 14 React deploy script auto-start
def react_p14_build():
    
    script_path = os.path.join(os.path.dirname(__file__), '../', 'build.sh')
    
    if os.path.exists(script_path):
    
        try:
    
            print('DEBUG (React Build) -> Exec BUILD.SH')

            subprocess.run(['bash', script_path], check=True)
            
            print('DEBUG (React Build) - Build.sh OK!!!')
    
        except subprocess.CalledProcessError as e:
            
            print(f"DEBUG (React Build) -> ERROR EXEC BUILD.SH: {str(e)}")
    
    else:
    
        print(f'DEBUG 14 -> BUILD.SH NOT FOUND!!! : {script_path}')

