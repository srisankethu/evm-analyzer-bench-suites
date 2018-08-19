import os
import re
import subprocess
import time

"""Analyser-related things"""

def get_analyser_prog(analyser):
    """Return the mythril program name to run. Setting a name inenvironent variable MYTH
    takes precidence of the vanilla name "myth". As a sanity check, try
    running this command with --version to make sure it does something.
    """

    if analyser == "Mythril":
        analyser_prog = os.environ.get('MYTH', 'myth')
    elif analyser == "Manticore":
        analyser_prog = os.environ.get('MANTICORE', 'manticore')

    cmd = [analyser_prog, '--version']
    s = subprocess.run(cmd, stdout=subprocess.PIPE)
    if s.returncode != 0:
        print("Failed to get run {} with:\n\t{}\n failed with return code {}"
              .format(analyser_prog, ' '.join(cmd), s.returncode))
        return None

    if analyser_prog == "myth":
        m = re.search('Mythril version (.+)', s.stdout.decode('utf-8'))
    elif analyser_prog == "manticore":
        m = re.search('Manticore (.+)', s.stdout.decode('utf-8'))

    if m:
        analyser_version = m.group(1)
    # FIXME: check version
    return analyser_prog, analyser_version

def run_analyser(analyser_prog, sol_file, debug, timeout):

    if analyser_prog == 'myth':
        cmd = [analyser_prog, '-x', '-o', 'json', '{}'.format(sol_file)]
    elif analyser_prog == 'manticore':
        cmd = [analyser_prog, '--detect-all', '{}'.format(sol_file)]

    if debug:
        print(' '.join(cmd))
    start = time.time()
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        result = None
    elapsed = (time.time() - start)
    return elapsed, result
