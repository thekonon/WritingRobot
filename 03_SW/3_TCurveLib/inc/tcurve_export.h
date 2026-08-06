#pragma once

#ifdef _WIN32
    #ifdef TCURVE_EXPORTS
        #define TCURVE_API __declspec(dllexport)
    #else
        #define TCURVE_API __declspec(dllimport)
    #endif
#else
    #define TCURVE_API
#endif