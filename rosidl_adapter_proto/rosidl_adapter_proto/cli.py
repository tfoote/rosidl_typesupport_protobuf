import argparse
import os
import pathlib
import sys

from ament_index_python import get_package_share_directory

from catkin_pkg.package import package_exists_at
from catkin_pkg.package import parse_package

from rosidl_adapter.action import convert_action_to_idl
from rosidl_adapter.msg import convert_msg_to_idl
from rosidl_adapter.srv import convert_srv_to_idl

from rosidl_cmake import read_generator_arguments

from rosidl_cli.command.helpers import interface_path_as_tuple
from rosidl_cli.command.helpers import legacy_generator_arguments_file
from rosidl_cli.command.translate.extensions import TranslateCommandExtension
from rosidl_cli.command.translate.api import translate

from rosidl_adapter_proto import generate_proto
from rosidl_adapter_proto import compile_proto

def convert_to_proto(generator_arguments_file, protoc_path):
    generator_args = read_generator_arguments(generator_arguments_file)

    # Generate .proto files
    rc = generate_proto(generator_arguments_file) 
    if rc :
        raise RuntimeError

    # Compile .proto files using protoc
    cpp_out_dir     = str(pathlib.Path(generator_args["output_dir"] + "/..").resolve())
    proto_path_list = [str(pathlib.Path(generator_args["output_dir"] + "/..").resolve())]
    proto_files     = []
    package_name    = generator_args["package_name"]

    if "additional_files" in generator_args:
        proto_path_list += generator_args["additional_files"]

    pathlib.Path(cpp_out_dir).mkdir(parents=True, exist_ok=True)

    for idl_tuple in generator_args.get('idl_tuples', []):
        idl_parts = idl_tuple.rsplit(':', 1)
        assert len(idl_parts) == 2
        idl_rel_path = pathlib.Path(idl_parts[1])
        idl_stem = idl_rel_path.stem
        generated_file = os.path.join(
                    generator_args['output_dir'],
                    str(idl_rel_path.parent),
                    idl_stem + ".proto"
        )
        proto_files.append(str(pathlib.Path(generated_file).resolve()))

    # compile proto files with protoc
    rc = compile_proto(protoc_path     = protoc_path,
                       proto_path_list = proto_path_list,
                       cpp_out_dir     = cpp_out_dir,
                       proto_files     = proto_files,
                       package_name    = package_name
    )
    if rc :
        raise RuntimeError

    return proto_files


def convert_files_to_idl(extension, conversion_function, argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description=f'Convert {extension} files to .idl')
    parser.add_argument(
        'interface_files', nargs='+',
        help='The interface files to convert')
    args = parser.parse_args(argv)

    for interface_file in args.interface_files:
        interface_file = pathlib.Path(interface_file)
        package_dir = interface_file.parent.absolute()
        while (
            len(package_dir.parents) and
            not package_exists_at(str(package_dir))
        ):
            package_dir = package_dir.parent
        if not package_dir.parents:
            print(
                f"Could not find package for '{interface_file}'",
                file=sys.stderr)
            continue
        warnings = []
        pkg = parse_package(package_dir, warnings=warnings)

        conversion_function(
            package_dir, pkg.name,
            interface_file.absolute().relative_to(package_dir),
            interface_file.parent)


class TranslateToProto(TranslateCommandExtension):

    output_format = 'proto'

    def translate(
        self,
        package_name,
        interface_files,
        include_paths,
        output_path
    ):

        generated_files = []

        package_share_path = pathlib.Path(
            get_package_share_directory('rosidl_adapter_proto'))
        templates_path = package_share_path / 'resource'


        idl_interface_files = []
        non_idl_interface_files = []
        for path in interface_files:
            if not path.endswith('.idl'):
                non_idl_interface_files.append(path)
            else:
                idl_interface_files.append(path)
        if non_idl_interface_files:
            idl_interface_files.extend(translate(
                package_name=package_name,
                interface_files=non_idl_interface_files,
                include_paths=include_paths,
                output_format='idl',
                output_path=output_path / 'tmp',
            ))


                # Generate code
        with legacy_generator_arguments_file(
            package_name=package_name,
            interface_files=idl_interface_files,
            include_paths=include_paths,
            templates_path=templates_path,
            output_path=output_path
        ) as path_to_arguments_file:
            generated_files.extend(convert_to_proto(path_to_arguments_file, '/usr/bin/protoc'))
        return generated_files



class TranslateMsgToProto(TranslateToProto):
    input_format = 'msg'


class TranslateSrvToProto(TranslateToProto):
    input_format = 'srv'


class TranslateActionToProto(TranslateToProto):
    input_format = 'action'
