import os
import stat

def audit_file(path):
    st = os.stat(path)
    mode = st.st_mode
    issues = []
    if mode & stat.S_IWOTH:
        issues.append('world-writable')
    if stat.S_ISREG(mode) and (mode & stat.S_IXUSR) and (mode & stat.S_IWOTH):
        issues.append('world-writable executable')
    if stat.S_ISDIR(mode) and not (mode & stat.S_ISVTX):
        if mode & stat.S_IWOTH:
            issues.append('world-writable directory without sticky bit')
    if mode & stat.S_ISUID:
        issues.append('setuid bit set')
    if mode & stat.S_ISGID:
        issues.append('setgid bit set')
    return {'path': path, 'mode': oct(stat.S_IMODE(mode)), 'issues': issues}

def audit_tree(root):
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            out.append(audit_file(os.path.join(dirpath, name)))
    return out
