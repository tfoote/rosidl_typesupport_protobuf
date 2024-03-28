import pytest
import os
import pathlib
import shutil
import subprocess

from ament_index_python import get_package_share_directory

def test_ts_files_generation():
    build_then_install('/tmp/tr')
    files_exists('/tmp/tr')

def build_then_install(output_path):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    package_share_path = pathlib.Path(
            get_package_share_directory('std_msgs'))
  
    subprocess.run([
        'rosidl', 'translate', '-o', output_path, '--from', 'msg', '--to', 'proto', 'std_msgs', './msg/String.msg'
    ], cwd=package_share_path, check=True)

def files_exists(output_path):
    assert pathlib.Path('/tmp/tr/msg/String.pb.cc').exists()
    assert pathlib.Path('/tmp/tr/msg/String.pb.h').exists()
    assert pathlib.Path('/tmp/tr/msg/String.proto').exists()
    assert pathlib.Path('/tmp/tr/tmp/msg/String.idl').exists()
    