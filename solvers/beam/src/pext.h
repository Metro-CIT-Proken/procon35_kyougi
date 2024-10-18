#pragma once

#if __x86_64__
    #pragma message ("Using native bmi2 pext instruction.")
    #include <x86intrin.h>
#else
    #pragma message ("Using fallback pext instruction.")
static unsigned long long int _pext_u64(unsigned long long int x, unsigned long long int mask) {
    unsigned long long int res = 0;
    int j = 0;
    for(int i = 0; i < 64; i++) {
        if((mask >> i) & 1) {
            res |= ((x >> i) & 1) << j;
            j++;
        }
    }
    return res;
}
#endif