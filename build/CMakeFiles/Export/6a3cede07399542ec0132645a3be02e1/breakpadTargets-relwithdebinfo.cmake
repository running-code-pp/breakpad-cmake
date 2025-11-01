#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "breakpad::breakpad_client" for configuration "RelWithDebInfo"
set_property(TARGET breakpad::breakpad_client APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(breakpad::breakpad_client PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELWITHDEBINFO "CXX"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/breakpad_client.lib"
  )

list(APPEND _cmake_import_check_targets breakpad::breakpad_client )
list(APPEND _cmake_import_check_files_for_breakpad::breakpad_client "${_IMPORT_PREFIX}/lib/breakpad_client.lib" )

# Import target "breakpad::breakpad_processor" for configuration "RelWithDebInfo"
set_property(TARGET breakpad::breakpad_processor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(breakpad::breakpad_processor PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELWITHDEBINFO "CXX"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/breakpad.lib"
  )

list(APPEND _cmake_import_check_targets breakpad::breakpad_processor )
list(APPEND _cmake_import_check_files_for_breakpad::breakpad_processor "${_IMPORT_PREFIX}/lib/breakpad.lib" )

# Import target "breakpad::disasm" for configuration "RelWithDebInfo"
set_property(TARGET breakpad::disasm APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(breakpad::disasm PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELWITHDEBINFO "C"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/disasm.lib"
  )

list(APPEND _cmake_import_check_targets breakpad::disasm )
list(APPEND _cmake_import_check_files_for_breakpad::disasm "${_IMPORT_PREFIX}/lib/disasm.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
