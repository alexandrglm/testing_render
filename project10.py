############################################################################
# Project 10: WebShell project using websockets
#
#
################
from flask import Blueprint, render_template, jsonify
from flask_socketio import emit, SocketIO
import subprocess
import os
############################################################################
# Blueprint project10
project10 = Blueprint('project10', __name__)

@project10.route('/')
def render_project_10():
    return render_template('10/index_10.html')

@project10.route('/API_Secrets')
def handling_secrets():

    uri = os.environ.get('shell_uri')

    return jsonify( { 'shell_uri': uri } )

###################################################
# exports
forbidden = (
    'rm', 'touch', 'dd', 'sudo', 'kill', ':(){ :|:& };:',
    'chmod', 'chown', 'mkfs', 'mount', 'umount', 'chroot',
    'reboot', 'shutdown', 'halt',
    'ln', 'mkdir', 'mv',
    'wget', 'curl', 
    'nc', 'ncat',
    'at', 'cron', 'crontab',
    'bash', 'sh', 'zsh',
    'python', 'perl', 'ruby',
    'free', 'top', 'vmstat', 'ps',
    'fallocate', 'truncate',
    'sync', 'ssh', 'ftp', 'sftp', 'tftp', 'screen', 'time',
    'passwd', 'gpg',
    'telnet', 'netstat', 'route', 'ip', 'ifconfig', 'iwconfig', 'iw', 'ping', 'traceroute', 'tracert',
    'fsck', 'fdisk', 'parted', 'gdisk', 'mkswap',
    'cat', 'echo', 'printf', 'tee', 'head', 'tail', 'paste', 'join',
    'find', 'locate', 'grep', 'sed', 'awk',
    'gzip', 'gunzip', 'bzip2', 'bunzip2', 'tar', 'zip', 'unzip',
    'gcc', 'g++', 'make',
    'ldconfig', 'ldd', 'objdump', 'nm',
    'strace', 'ltrace',
    'iptables', 'ufw',
    'systemctl', 'service',
    'useradd', 'userdel', 'groupadd', 'groupdel',
    'dpkg', 'apt',
    'vi', 'vim', 'nano', 'emacs',
    'xargs', 'sort', 'uniq', 'cut', 'tr',
    'ld', 'ar', 'ranlib', 'strip',
    'tcpdump', 'wireshark',
    'mke2fs',
    'losetup', 'mdadm', 'dmsetup',
    'setfacl', 'getfacl',
    'chattr', 'lsattr',
    'rename', 'install',
    'readlink', 'realpath',
    'export', 'source',
    'nohup', 'disown',
    'file', 'ldd', 'string',
    'eval',
    './', '~/', '(', '/', '$'
)

def commander(data):

    try:
        
        command = data.get('command', '').strip()

        if len(command) > 60:
            
            emit('commander_output', {'output': f'Sorry, the lengtf of the queries should be reduced!'})
            return

        for f in forbidden:
            
            if command.startswith(forbidden):
                
                emit('commander_output', {'output': f'Sorry, "{command}" is locked for execution!'})
                return
        

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        output = result.stdout if result.returncode == 0 else result.stderr
        emit('commander_output', {'output': output})
    
    except Exception as e:
        
        emit('commander_output', {'output': f"Error Command Exec: {str(e)}"})