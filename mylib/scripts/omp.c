#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LL long long 

int main(int argc, char* argv[]){
    if(argc != 3){
        return -1;
    }
    LL limit = atoll(argv[1]);
    int thread_cnt = atoll(argv[2]);

    #pragma omp parallel for num_threads(thread_cnt)
    for(LL i = 0; i < limit; i++){
        // nop
    }

    return 0;
}
