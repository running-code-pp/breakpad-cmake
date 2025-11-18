cmake_minimum_required(VERSION 3.15)
project(breakpad VERSION 2024.02.16 LANGUAGES CXX C)

# 选项
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
option(BREAKPAD_BUILD_PROCESSOR "Build breakpad processor library" ON)
option(BREAKPAD_BUILD_CLIENT "Build breakpad client library" ON)
option(BREAKPAD_BUILD_TOOLS "Build breakpad tools" OFF)

# 设置 C++11 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 99)

# 包含目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/breakpad-2024.02.16/src
)

# 平台检测
if(WIN32)
    set(BREAKPAD_PLATFORM "windows")
    add_definitions(-DUNICODE -D_UNICODE)
    # Windows 特定的定义
    add_definitions(-DWIN32_LEAN_AND_MEAN -DNOMINMAX)
elseif(UNIX AND NOT APPLE)
    set(BREAKPAD_PLATFORM "linux")
    # Linux 特定的定义
    add_definitions(-DHAVE_A_OUT_H)
elseif(APPLE)
    set(BREAKPAD_PLATFORM "mac")
endif()

# =============================================================================
# Breakpad 通用源文件
# =============================================================================
set(BREAKPAD_COMMON_SOURCES
    breakpad-2024.02.16/src/common/convert_UTF.cc
    breakpad-2024.02.16/src/common/convert_UTF.h
    breakpad-2024.02.16/src/common/md5.cc
    breakpad-2024.02.16/src/common/md5.h
    breakpad-2024.02.16/src/common/string_conversion.cc
    breakpad-2024.02.16/src/common/string_conversion.h
)

# =============================================================================
# Windows 客户端库
# =============================================================================
if(WIN32 AND BREAKPAD_BUILD_CLIENT)
    set(BREAKPAD_CLIENT_WINDOWS_SOURCES
        breakpad-2024.02.16/src/client/windows/crash_generation/client_info.cc
        breakpad-2024.02.16/src/client/windows/crash_generation/crash_generation_client.cc
        breakpad-2024.02.16/src/client/windows/crash_generation/crash_generation_server.cc
        breakpad-2024.02.16/src/client/windows/handler/exception_handler.cc
        breakpad-2024.02.16/src/client/windows/sender/crash_report_sender.cc
        breakpad-2024.02.16/src/common/windows/guid_string.cc
        breakpad-2024.02.16/src/common/windows/http_upload.cc
        breakpad-2024.02.16/src/common/windows/string_utils.cc
    )

    add_library(breakpad_client ${BREAKPAD_CLIENT_WINDOWS_SOURCES} ${BREAKPAD_COMMON_SOURCES})
    
    target_include_directories(breakpad_client PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/breakpad-2024.02.16/src>
        $<INSTALL_INTERFACE:include>
    )

    target_link_libraries(breakpad_client PRIVATE wininet.lib)

    set_target_properties(breakpad_client PROPERTIES
        PUBLIC_HEADER "breakpad-2024.02.16/src/client/windows/handler/exception_handler.h"
        OUTPUT_NAME "breakpad_client"
    )
endif()

# =============================================================================
# Linux 客户端库
# =============================================================================
if(UNIX AND NOT APPLE AND BREAKPAD_BUILD_CLIENT)
    # 检查是否有 getcontext 函数
    include(CheckFunctionExists)
    check_function_exists(getcontext HAVE_GETCONTEXT)

    set(BREAKPAD_CLIENT_LINUX_SOURCES
        breakpad-2024.02.16/src/client/linux/crash_generation/crash_generation_client.cc
        breakpad-2024.02.16/src/client/linux/crash_generation/crash_generation_server.cc
        breakpad-2024.02.16/src/client/linux/dump_writer_common/thread_info.cc
        breakpad-2024.02.16/src/client/linux/dump_writer_common/ucontext_reader.cc
        breakpad-2024.02.16/src/client/linux/handler/exception_handler.cc
        breakpad-2024.02.16/src/client/linux/handler/minidump_descriptor.cc
        breakpad-2024.02.16/src/client/linux/log/log.cc
        breakpad-2024.02.16/src/client/linux/microdump_writer/microdump_writer.cc
        breakpad-2024.02.16/src/client/linux/minidump_writer/linux_core_dumper.cc
        breakpad-2024.02.16/src/client/linux/minidump_writer/linux_dumper.cc
        breakpad-2024.02.16/src/client/linux/minidump_writer/linux_ptrace_dumper.cc
        breakpad-2024.02.16/src/client/linux/minidump_writer/minidump_writer.cc
        breakpad-2024.02.16/src/client/linux/minidump_writer/pe_file.cc
        breakpad-2024.02.16/src/client/minidump_file_writer.cc
        breakpad-2024.02.16/src/common/linux/elf_core_dump.cc
        breakpad-2024.02.16/src/common/linux/elfutils.cc
        breakpad-2024.02.16/src/common/linux/file_id.cc
        breakpad-2024.02.16/src/common/linux/guid_creator.cc
        breakpad-2024.02.16/src/common/linux/linux_libc_support.cc
        breakpad-2024.02.16/src/common/linux/memory_mapped_file.cc
        breakpad-2024.02.16/src/common/linux/safe_readlink.cc
        ${BREAKPAD_COMMON_SOURCES}
    )

    if(NOT HAVE_GETCONTEXT)
        list(APPEND BREAKPAD_CLIENT_LINUX_SOURCES
            breakpad-2024.02.16/src/common/linux/breakpad_getcontext.S
        )
    endif()

    add_library(breakpad_client ${BREAKPAD_CLIENT_LINUX_SOURCES})

    target_include_directories(breakpad_client PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/breakpad-2024.02.16/src>
        $<INSTALL_INTERFACE:include>
    )

    target_link_libraries(breakpad_client PRIVATE pthread dl)

    set_target_properties(breakpad_client PROPERTIES
        PUBLIC_HEADER "breakpad-2024.02.16/src/client/linux/handler/exception_handler.h"
        OUTPUT_NAME "breakpad_client"
        POSITION_INDEPENDENT_CODE ON
    )
endif()

# =============================================================================
# Breakpad Processor 库
# =============================================================================
if(BREAKPAD_BUILD_PROCESSOR)
    set(BREAKPAD_PROCESSOR_SOURCES
        breakpad-2024.02.16/src/processor/basic_code_modules.cc
        breakpad-2024.02.16/src/processor/basic_source_line_resolver.cc
        breakpad-2024.02.16/src/processor/call_stack.cc
        breakpad-2024.02.16/src/processor/cfi_frame_info.cc
        breakpad-2024.02.16/src/processor/convert_old_arm64_context.cc
        breakpad-2024.02.16/src/processor/disassembler_x86.cc
        breakpad-2024.02.16/src/processor/dump_context.cc
        breakpad-2024.02.16/src/processor/dump_object.cc
        breakpad-2024.02.16/src/processor/exploitability.cc
        breakpad-2024.02.16/src/processor/exploitability_linux.cc
        breakpad-2024.02.16/src/processor/exploitability_win.cc
        breakpad-2024.02.16/src/processor/fast_source_line_resolver.cc
        breakpad-2024.02.16/src/processor/logging.cc
        breakpad-2024.02.16/src/processor/microdump.cc
        breakpad-2024.02.16/src/processor/microdump_processor.cc
        breakpad-2024.02.16/src/processor/minidump.cc
        breakpad-2024.02.16/src/processor/minidump_processor.cc
        breakpad-2024.02.16/src/processor/module_comparer.cc
        breakpad-2024.02.16/src/processor/module_serializer.cc
        breakpad-2024.02.16/src/processor/pathname_stripper.cc
        breakpad-2024.02.16/src/processor/process_state.cc
        breakpad-2024.02.16/src/processor/proc_maps_linux.cc
        breakpad-2024.02.16/src/processor/simple_symbol_supplier.cc
        breakpad-2024.02.16/src/processor/source_line_resolver_base.cc
        breakpad-2024.02.16/src/processor/stack_frame_cpu.cc
        breakpad-2024.02.16/src/processor/stack_frame_symbolizer.cc
        breakpad-2024.02.16/src/processor/stackwalk_common.cc
        breakpad-2024.02.16/src/processor/stackwalker.cc
        breakpad-2024.02.16/src/processor/stackwalker_amd64.cc
        breakpad-2024.02.16/src/processor/stackwalker_arm.cc
        breakpad-2024.02.16/src/processor/stackwalker_arm64.cc
        breakpad-2024.02.16/src/processor/stackwalker_address_list.cc
        breakpad-2024.02.16/src/processor/stackwalker_mips.cc
        breakpad-2024.02.16/src/processor/stackwalker_ppc.cc
        breakpad-2024.02.16/src/processor/stackwalker_ppc64.cc
        breakpad-2024.02.16/src/processor/stackwalker_riscv.cc
        breakpad-2024.02.16/src/processor/stackwalker_riscv64.cc
        breakpad-2024.02.16/src/processor/stackwalker_sparc.cc
        breakpad-2024.02.16/src/processor/stackwalker_x86.cc
        breakpad-2024.02.16/src/processor/symbolic_constants_win.cc
        breakpad-2024.02.16/src/processor/tokenize.cc
        ${BREAKPAD_COMMON_SOURCES}
    )
    
    # Linux 特定的处理器源文件
    if(UNIX AND NOT APPLE)
        list(APPEND BREAKPAD_PROCESSOR_SOURCES
            breakpad-2024.02.16/src/processor/disassembler_objdump.cc
            breakpad-2024.02.16/src/common/linux/scoped_pipe.cc
            breakpad-2024.02.16/src/common/linux/scoped_tmpfile.cc
        )
    endif()
    
    add_library(breakpad_processor ${BREAKPAD_PROCESSOR_SOURCES})
    
    target_include_directories(breakpad_processor PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/breakpad-2024.02.16/src>
        $<INSTALL_INTERFACE:include>
    )
    
    if(UNIX)
        target_link_libraries(breakpad_processor PRIVATE pthread)
    endif()
    
    set_target_properties(breakpad_processor PROPERTIES
        OUTPUT_NAME "breakpad_processor"
        POSITION_INDEPENDENT_CODE ON
    )
endif()

# =============================================================================
# libdisasm (第三方库, Windows 需要)
# =============================================================================
if(WIN32 AND BREAKPAD_BUILD_PROCESSOR)
    set(LIBDISASM_SOURCES
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_implicit.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_insn.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_invariant.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_modrm.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_opcode_tables.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_operand.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_reg.c
        breakpad-2024.02.16/src/third_party/libdisasm/ia32_settings.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_disasm.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_format.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_imm.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_insn.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_misc.c
        breakpad-2024.02.16/src/third_party/libdisasm/x86_operand_list.c
    )
    
    add_library(disasm ${LIBDISASM_SOURCES})
    target_include_directories(disasm PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/breakpad-2024.02.16/src>
    )
    
    if(TARGET breakpad_processor)
        target_link_libraries(breakpad_processor PRIVATE disasm)
    endif()
endif()

# =============================================================================
# 安装规则
# =============================================================================
include(GNUInstallDirs)

# 收集所有要安装的目标
set(BREAKPAD_TARGETS)

if(TARGET breakpad_client)
    list(APPEND BREAKPAD_TARGETS breakpad_client)
endif()

if(TARGET breakpad_processor)
    list(APPEND BREAKPAD_TARGETS breakpad_processor)
endif()

if(TARGET disasm)
    list(APPEND BREAKPAD_TARGETS disasm)
endif()

# 安装库
if(BREAKPAD_TARGETS)
    install(TARGETS ${BREAKPAD_TARGETS}
        EXPORT breakpadTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

# 安装头文件 - 只安装公共 API 头文件
if(BREAKPAD_BUILD_CLIENT)
    # Google Breakpad 公共头文件
    install(DIRECTORY breakpad-2024.02.16/src/google_breakpad/
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/google_breakpad
        FILES_MATCHING PATTERN "*.h"
    )
    
    # Windows 客户端头文件
    if(WIN32)
        install(DIRECTORY breakpad-2024.02.16/src/client/windows/
            DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/client/windows
            FILES_MATCHING PATTERN "*.h"
        )
    endif()
    
    # Linux 客户端头文件
    if(UNIX AND NOT APPLE)
        install(DIRECTORY breakpad-2024.02.16/src/client/linux/
            DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/client/linux
            FILES_MATCHING PATTERN "*.h"
        )
    endif()
    
    # 通用客户端头文件
    install(FILES
        breakpad-2024.02.16/src/client/minidump_file_writer.h
        breakpad-2024.02.16/src/client/minidump_file_writer-inl.h
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/client
    )
endif()

if(BREAKPAD_BUILD_PROCESSOR)
    # 处理器公共头文件
    install(DIRECTORY breakpad-2024.02.16/src/processor/
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/processor
        FILES_MATCHING PATTERN "*.h"
    )
endif()

# 安装通用头文件
install(DIRECTORY breakpad-2024.02.16/src/common/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/common
    FILES_MATCHING PATTERN "*.h"
)

# 导出目标
install(EXPORT breakpadTargets
    FILE breakpadTargets.cmake
    NAMESPACE breakpad::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/breakpad
)

# 创建配置文件
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/breakpadConfigVersion.cmake"
    VERSION "2024.02.16"
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/breakpadConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/breakpad
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/breakpadConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/breakpadConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/breakpad
)
