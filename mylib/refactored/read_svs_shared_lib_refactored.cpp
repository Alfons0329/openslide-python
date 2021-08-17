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
    int read_region_cpp(uint32_t*, const char*, const float, const int, uint32_t&, uint32_t&);
}

int read_region_cpp(uint32_t* buf, const char* slide_path, const float resize_ratio_in, const int thread_cnt, uint32_t& target_width_in, uint32_t& target_height_in){
    float resize_ratio = resize_ratio_in;
    int32_t target_level = 0;
    int64_t target_width = 0, target_height = 0;
    int level_cnt;
    
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
    target_width_in = target_width;
    target_height_in = target_height;

    openslide_read_region(slide, buf, 0, 0, target_level, target_width, target_height);

    // ARGB2RGBA
    const uint32_t slide_dimension = target_width * target_height;
    #pragma omp parallel for num_threads(32)
    for(uint32_t i = 0; i < slide_dimension; i++){
        uint32_t a = (buf[i] >> 24) & 0xff;
        uint32_t r = (buf[i] >> 16) & 0xff;
        uint32_t g = (buf[i] >>  8) & 0xff;
        uint32_t b = (buf[i] >>  0) & 0xff;

        // ABGR (Correct, confirmed, little-endian)
        buf[i] = (a << 24U | b << 16U | g << 8U | r) & 0xffffffff;
    }

    openslide_close(slide);
    if(chk_err(slide)){
        return 5;
    }

    return EXIT_SUCCESS;
}