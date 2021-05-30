#include "openslide-features.h"
#include "openslide.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <chrono>
#include <omp.h>
#include <math.h>

#define RED   "\x1B[31m"
#define GRN   "\x1B[32m"
#define YEL   "\x1B[33m"
#define BLU   "\x1B[34m"
#define MAG   "\x1B[35m"
#define CYN   "\x1B[36m"
#define WHT   "\x1B[37m"
#define RESET "\x1B[0m"

int chk_err(openslide_t* osr){
    const char* err_str = openslide_get_error(osr);
    if(err_str != NULL){
        fprintf(stderr, "\t[C++ ERROR] Openslide_error: %s, ignore this slide\n", err_str);
        return 1;
    }
    return 0;
}
extern "C"{
    float read_region_cpp(uint32_t*, const char*, const int, const int thread_cnt);
}

int read_region_cpp(uint32_t* buf, const char* slide_path, const float resize_ratio_in,const int thread_cnt){
    float resize_ratio = resize_ratio_in;
    int32_t target_level = 0;
    int64_t target_width = 0, target_height = 0;
    int level_cnt;

    // Some setup functions
    openslide_t* slide = openslide_open(slide_path);
    if(chk_err(slide)){
        return 1;
    }
    level_cnt = openslide_get_level_count(slide);
    if(chk_err(slide)){
        return 2;
    }
    for(int i = 0; i < level_cnt; i++){
        int32_t tmp_level = openslide_get_level_downsample(slide, i);
        if(chk_err(slide)){
            return 3;
        }
        if(tmp_level <= 1.0 / resize_ratio){
            target_level = i;
        }
    }
    openslide_get_level_dimensions(slide, target_level, &target_width, &target_height);
    if(chk_err(slide)){
        return 4;
    }

    // Openslide parallel read WSIs
    const uint32_t thr = thread_cnt;
    const uint32_t target_height_round_up = ceil((float)target_height / thread_cnt) * thread_cnt;
    const uint32_t target_height_remain = target_height - ceil((float)target_height / thread_cnt) * (thread_cnt - 1);
    const uint32_t segment_y = target_height_round_up / thr;
    const uint32_t chunksize = target_width * target_height_round_up / thr;
    
    #pragma omp parallel for num_threads(thr)
    for(uint32_t i = 0; i < thr; i++){
        if(i == thr - 1){
            openslide_read_region(slide, buf + chunksize * i, 0, 4 * segment_y * i, target_level, target_width, target_height_remain);
        }
        else{
            openslide_read_region(slide, buf + chunksize * i, 0, 4 * segment_y * i, target_level, target_width, segment_y);
        }
    }

    // ARGB2RGBA
    const uint32_t slide_dimension = target_width * target_height;
    #pragma omp parallel for num_threads(32)
    for(uint32_t i = 0; i < slide_dimension; i++){
        uint32_t a = (buf[i] >> 24) & 0xff;
        uint32_t r = (buf[i] >> 16) & 0xff;
        uint32_t g = (buf[i] >>  8) & 0xff;
        uint32_t b = (buf[i] >>  0) & 0xff;

        // ABGR (Correct, confirmed)
        buf[i] = (a << 24U | b << 16U | g << 8U | r) & 0xffffffff;
    }

    openslide_close(slide);
    if(chk_err(slide)){
        return 5;
    }

    return overhead_load_image;
}

#define MAX_N 40000
int main(int argc, char **argv){
    uint32_t* buf = (uint32_t*) malloc(sizeof(uint32_t) * MAX_N * MAX_N);
    if(argc != 4){
        fprintf(stderr, "%s", "Usage: ./out slide_path, method, thread_cnt");
        return -1;
    }
    read_region_cpp(buf, argv[1], atoi(argv[2]), atoi(argv[3]));

    return 0;
}
/*
// 128 method with thread-pool
        else if(method == 5){
            gettimeofday(&begin, NULL);
            const uint32_t task_height = TASK_H;
            #pragma omp parallel for num_threads(thr)
            for(uint32_t i = 0; i < target_height; i += task_height){
                openslide_read_region(slide, buf + i * target_width, 0, 4 * i, target_level, target_width, 128);
            }
            gettimeofday(&end, NULL);
        }
*/