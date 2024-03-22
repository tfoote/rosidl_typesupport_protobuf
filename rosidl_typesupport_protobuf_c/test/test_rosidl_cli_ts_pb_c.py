import pytest
import os
import pathlib
import shutil
import subprocess


def test_ts_files_generation():
    build_then_install('/tmp/pb')
    files_exists('/tmp/pb')

def build_then_install(output_path):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

#rosidl generate -ts protobuf_c -o /tmp/pb std_msgs ./install/std_msgs/share/std_msgs/msg/String.msg

    subprocess.run([
        'rosidl', 'generate', '-ts', 'protobuf_c', '-o', output_path, 'std_msgs', './msg/String.msg'
    ], cwd='/home/aeten/ros2_rolling/install/std_msgs/share/std_msgs', check=True)

def files_exists(output_path):
    assert pathlib.Path('/tmp/pb/tmp/msg/String.idl').exists()
    assert pathlib.Path('/tmp/pb/msg/rosidl_typesupport_protobuf_c__visibility_control.h').exists()
    assert pathlib.Path('/tmp/pb/msg/string__rosidl_typesupport_protobuf_c.hpp').exists()
    assert pathlib.Path('/tmp/pb/msg/detail/string__type_support.cpp').exists()
    