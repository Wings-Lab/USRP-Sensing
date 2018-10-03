cmake_minimum_required(VERSION 2.8.12)
project(NotificationDemo CXX)

add_executable(app rtl-network.cpp )

target_link_libraries(app rtlsdr)
