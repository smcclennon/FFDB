# Flat File Database
# github.com/smcclennon/FFDB
ver = '1.0.0'
proj = 'FFDB'


databaseDIR = 'word database'


import time, itertools, os, urllib.request, json
from distutils.version import LooseVersion as semver
from os.path import isfile, join



# -==========[ Update code ]==========-
# Updater: Used to check for new releases on GitHub
# github.com/smcclennon/Updater
import os  # detecting OS type (nt, posix, java), clearing console window, restart the script
from distutils.version import LooseVersion as semver  # as semver for readability
import urllib.request, json  # load and parse the GitHub API
import platform  # Consistantly detect MacOS

# Disable SSL certificate verification for MacOS (very bad practice, I know)
# https://stackoverflow.com/a/55320961
if platform.system() == 'Darwin':  # If MacOS
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

if os.name == 'nt':
    import ctypes  # set Windows console window title
    ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==   Checking for updates...')

updateAttempt = 0  # Keep track of failed attempts
print('Checking for updates...', end='\r')
while updateAttempt < 3:  # Try to retry the update up to 3 times if an error occurs
    updateAttempt = updateAttempt+1
    try:
        with urllib.request.urlopen("https://smcclennon.github.io/update/api/4") as internalAPI:
            repo = []
            for line in internalAPI.readlines():
                repo.append(line.decode().strip())
            apiLatest = repo[0]  # Latest release details
            proj = repo[1]  # Project name
            ddl = repo[2]  # Direct download link
            apiReleases = repo[3]  # List of patch notes
        with urllib.request.urlopen(apiLatest) as githubAPILatest:
            data = json.loads(githubAPILatest.read().decode())
            latest = data['tag_name'][1:]  # remove 'v' from version number (v1.2.3 -> 1.2.3)
        del data  # Prevent overlapping variable data
        release = json.loads(urllib.request.urlopen(  # Get latest patch notes
            apiReleases).read().decode())
        releases = [  # Store latest patch notes in a list
            (data['tag_name'], data['body'])
            for data in release
            if semver(data['tag_name'][1:]) > semver(ver)]
        updateAttempt = 3
    except:  # If updating fails 3 times
        latest = '0'
if semver(latest) > semver(ver):
    if os.name == 'nt': ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==   Update available: {ver} -> {latest}')
    print('Update available!      ')
    print(f'Latest Version: v{latest}\n')
    for release in releases:
        print(f'{release[0]}:\n{release[1]}\n')
    confirm = input(str('Update now? [Y/n] ')).upper()
    if confirm != 'N':
        if os.name == 'nt': ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==   Installing updates...')
        print(f'Downloading {proj} v{latest}...')
        urllib.request.urlretrieve(ddl, os.path.basename(__file__))  # download the latest version to cwd
        import sys; sys.stdout.flush()  # flush any prints still in the buffer
        os.system('cls||clear')  # Clear console window
        os.system(f'"{__file__}"' if os.name == 'nt' else f'python3 "{__file__}"')
        import time; time.sleep(0.2)
        quit()
if os.name == 'nt': ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==')
# -==========[ Update code ]==========-




print(f'Loading {databaseDIR}...', end='\r')
start = time.time()
databaseFiles = [f for f in os.listdir(databaseDIR) if isfile(join(databaseDIR, f))]
fileCount = 0
databaseWords = []
for File in databaseFiles:
    with open(f'{databaseDIR}/{File}') as word_file:
        databaseWords = databaseWords + (word_file.read().lower().splitlines())
        fileCount = fileCount + 1
        print(f'Loading {databaseDIR}... ({fileCount})', end='\r')
    #print(f'Loaded "{File}"')
print(f'Loading {databaseDIR}... Done!')
print(f'Sorting database...', end='\r')
databaseWords = sorted(set(databaseWords))
print(f'Sorting database... Done!')
loadtime = time.time() - start
print(f'Loaded {len(databaseWords):,} words from {fileCount} files in {round(loadtime, 2)} seconds')



print(f'\nEnter a word to compare it against our database\nType .combo to brute force the English language')
while True:
    testword = input('\n> ').lower()
    if testword in databaseWords:
        wordIndex = list(databaseWords).index(testword)
        DBComparison = list(databaseWords)[wordIndex]
        print(f'"{DBComparison[0].upper()+DBComparison[1:]}" is number {wordIndex:,} in our dictionary')

    elif testword == '.combo':
        # Brute force code
        i=0
        with open(f'savecombo.txt', 'a') as f:
            for L in range(0, len(databaseWords)+1):
                for subset in itertools.combinations(databaseWords, L):
                    y = ", ".join(subset)
                    f.write(f'{y}\n')
                    print(f'[{i:,}]: {y}')
                    i+=1

    else:
        print(f'"{testword}" not in our dictionary')