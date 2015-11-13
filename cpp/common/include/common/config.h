#ifndef COMMON_CONFIG_H
#define COMMON_CONFIG_H

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)

#define VERSION_MAJOR 0
#define VERSION_MINOR 1

#define DEFAULT_LOCAL_HOSTNAME "127.0.0.1"
#define DEFAULT_LOCAL_INTERFACE "0.0.0.0"
#define DEFAULT_LOCAL_PORT 20000
#define DEFAULT_MEDIATOR_HOSTNAME "127.0.0.1"
#define DEFAULT_MEDIATOR_PORT 20000

#endif
