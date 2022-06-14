cmake_minimum_required(VERSION 3.16)

project(integrals VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTORCC ON)                   #for compiling qrc file to rcc
set(AUTORCC_OPTIONS "resources.qrc")

find_package(Qt6 6.2 COMPONENTS Quick REQUIRED)

qt_add_executable(appintegrals
    resources.qrc
    loadermanager.h loadermanager.cpp
    main.cpp
)

qt_add_qml_module(appintegrals
    URI integrals
    VERSION 1.0
    QML_FILES main.qml auth.qml splash.qml
)

set_target_properties(appintegrals PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_compile_definitions(appintegrals
    PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:QT_QML_DEBUG>)
target_link_libraries(appintegrals
    PRIVATE Qt6::Quick)
set(QML_IMPORT_PATH ${CMAKE_SOURCE_DIR}/qml ${CMAKE_BINARY_DIR}/imports CACHE STRING "" FORCE)
