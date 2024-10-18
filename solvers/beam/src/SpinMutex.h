// original
// https://github.com/taiheioki/procon2014_ut/blob/master/solver/modules/util/include/util/SpinMutex.hpp

#pragma once

#include <atomic>
#include <mutex>

class SpinMutex
{
private:
    std::atomic_bool locked;

public:
    SpinMutex() : locked(false) {}

    void lock() {
        while(locked.exchange(true, std::memory_order_acquire));
    }

    void unlock() {
        locked.store(false, std::memory_order_release);
    }
};