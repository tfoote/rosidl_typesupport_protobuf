import pytest
import os
import pathlib
import shutil
import subprocess

from ament_index_python import get_package_share_directory

def test_ts_files_generation():
    build_then_install('/tmp/pb')
    files_exists('/tmp/pb')

def build_then_install(output_path):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    package_share_path = pathlib.Path(
            get_package_share_directory('std_msgs'))
  
    subprocess.run([
        'rosidl', 'generate', '-ts', 'protobuf_c', '-o', output_path, 'std_msgs', './msg/String.msg'
    ], cwd=package_share_path, check=True)

def files_exists(output_path):
    assert pathlib.Path('/tmp/pb/tmp/msg/String.idl').exists()
    assert pathlib.Path('/tmp/pb/msg/rosidl_typesupport_protobuf_c__visibility_control.h').exists()
    assert pathlib.Path('/tmp/pb/msg/string__rosidl_typesupport_protobuf_c.hpp').exists()
    assert pathlib.Path('/tmp/pb/msg/detail/string__type_support.cpp').exists()
    