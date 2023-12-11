# Protobuf ROS Interface Design (Deep Structure)

## Type Specific Interface
The following diagram shows the system to perform type-specific functions to support .msg and .proto files. 

 <p align="center">
        <img src ="images/flow_chart_type_support_generation.png" width = "600"/>
       </p>

The left-hand side of the diagram shows how the .msg files are passed to the specific code generators (using vendors or rosidl_generator). The other side shows how the .proto files are passed to the code generators. Finally, the Type adapter block converter from one type to another (proto to msg, or .msg to proto), see [About-Internal-Interfaces](https://docs.ros.org/en/humble/Concepts/Advanced/About-Internal-Interfaces.html) for more information. 


## Specification
#### Type Adapter
To adapt the prototype message to a ROS type, protobuf type support generates a specialization for the proto message. The specialization has the following:
* is_specialized is always set to  std::true_type,
* Specify the proto custom type using custom =
* Specify the ROS type using ros_message
* Provide static convert functions with the signatures:
  * static void convert_to_ros_message(const custom_type &, ros_message_type &),
  * static void convert_to_custom(const ros_message_type &, custom_type &)


The convert function must convert from one type to the other, see [Type Adaptation Feature](https://ros.org/reps/rep-2007.html) for more information.

For example, the specialization for adapting std_msgs::msg::pb::String to the std_msgs_msg::String ROS message type:

```cpp
template<>
 struct TypeAdapter<::std_msgs::msg::pb::String,  ::std_msgs::msg::String>
 {
   using is_specialized = std::true_type;
   using custom_type = ::std_msgs::msg::pb::String;
   using ros_message_type =  ::std_msgs::msg::String;


   static
   void
   convert_to_ros_message(
    const custom_type & source,
    ros_message_type & destination)
   {
    std_msgs::msg::typesupport_protobuf_cpp::convert_to_ros(source, destination);
   }


   static
   void
   convert_to_custom(
     const ros_message_type & source,
     custom_type & destination)
   {
     std_msgs::msg::typesupport_protobuf_cpp::convert_to_proto(source, destination);
   }
 };

```

#### Mapping from IDL -> Protobuf Type:
This adapter also mapping from IDL types to Protobuf type.
[IDL to Protobuf type.](rosidl_adapter_proto/rosidl_adapter_proto/__init__.py)