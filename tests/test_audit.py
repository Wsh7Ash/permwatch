import os, pytest
from permwatch.audit import audit_file

def test_world_writable(tmp_path):
    f = tmp_path / 'ww.txt'
    f.write_text('x')
    os.chmod(f, 0o666)
    res = audit_file(str(f))
    assert 'world-writable' in res['issues']

@pytest.mark.skipif(os.name == 'nt', reason='Windows chmod only toggles the read-only flag; POSIX mode bits are not represented in stat')
def test_normal_file_clean(tmp_path):
    f = tmp_path / 'ok.txt'
    f.write_text('x')
    os.chmod(f, 0o644)
    res = audit_file(str(f))
    assert res['issues'] == []
