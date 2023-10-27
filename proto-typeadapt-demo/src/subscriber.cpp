// Copyright 2021 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <functional>
#include <memory>
#include <string>

#include "rclcpp/type_adapter.hpp"
#include "rclcpp/rclcpp.hpp"

#include "std_msgs/msg/string.hpp"
#include "std_msgs/rosidl_adapter_proto__visibility_control.h"
#include "std_msgs/msg/String.pb.h"
#include "std_msgs/msg/string__typeadapter_protobuf_cpp.hpp"

using std::placeholders::_1;

/* Normally a TypeAdapter specialization like this would go in a header
 * and be reused by the publisher and subscriber rather than copy-pasted
 * like this. We chose to include this here because it makes this example
 * more "self-contained". */


class MinimalSubscriber : public rclcpp::Node
{

using MyAdaptedType = rclcpp::TypeAdapter<std_msgs::msg::pb::String, std_msgs::msg::String>;


public:
  MinimalSubscriber()
  : Node("minimal_subscriber")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));

    subscription2_ = this->create_subscription<MyAdaptedType>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback2, this, _1));
  }

private:
  void topic_callback(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }

  void topic_callback2(const std_msgs::msg::pb::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard Proto: '%s'", msg.data().c_str());
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
  rclcpp::Subscription<MyAdaptedType>::SharedPtr subscription2_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}