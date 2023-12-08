/* ================================ Apache 2.0 =================================
 *
 * Copyright (C) 2021 Continental
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * ================================ Apache 2.0 =================================
 */

#pragma once

#include <rosidl_typesupport_protobuf/visibility_control.h>

#include <string>


namespace rosidl_typesupport_protobuf_cpp
{

ROSIDL_TYPESUPPORT_PROTOBUF_PUBLIC
void write_to_string(const std::u16string & u16str, std::string & str);

ROSIDL_TYPESUPPORT_PROTOBUF_PUBLIC
void write_to_u16string(const std::string & str, std::u16string & u16str);

}
