# Protobuf ROS Interface Design
## Abstract
This project provides the ability to publish and subscribe with Protobuf Datatypes to ROS native publishers and subscribers. So the user could work with the ROS native messages or use the Protobuf Datatypes.

## Example Usage

#### Dependencies

* The type adapter that allows the user to publish from native ROS message or Protobuf data type
    ```cpp
    #include "rclcpp/type_adapter.hpp"
    ```

* Next include the message to publish-subscribe, for example, a `string` message from `std_msgs`.
    ```cpp
    #include "std_msgs/msg/string.hpp"
    #include "std_msgs/msg/String.pb.h"
    ```

* Finally, include the type adapter for the Protobuf data type message.
    ```cpp
    #include "std_msgs/rosidl_adapter_proto__visibility_control.h"
    #include "std_msgs/msg/string__typeadapter_protobuf_cpp.hpp"
    ```
#### Publisher Example
```cpp
using MyAdaptedType = rclcpp::TypeAdapter<std_msgs::msg::pb::String, std_msgs::msg::String>;
publisher_ = this->create_publisher<MyAdaptedType>("topic", 10);
```
To publish a message, it is only required to specify the adapter type to send the topic.

#### Subscriber Example
```cpp
using MyAdaptedType = rclcpp::TypeAdapter<std_msgs::msg::pb::String, std_msgs::msg::String>;
subscription2_ = this->create_subscription<MyAdaptedType>(
     "topic", 10, std::bind(&MinimalSubscriber::topic_callback2, this, _1));
void topic_callback2(const std_msgs::msg::pb::String & msg) const
 {
   RCLCPP_INFO(this->get_logger(), "I heard Proto: '%s'", msg.data().c_str());
 }
```
To subscribe to the topic the user needs to specify the adapter type, and for the callback specify the protobuf message to hear the message received.

Another path to hear the message is using the ROS types messages:

```cpp
subscription_ = this->create_subscription<std_msgs::msg::String>(
     "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
void topic_callback(const std_msgs::msg::String & msg) const
 {
   RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
 }

```

To understand more about the internal structure go to [DEEP STRUCTURE](DEEP_STRUCTURE.md) seccion.