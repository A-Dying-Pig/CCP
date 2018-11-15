<template>
    <div class="index-slider" >
        <el-carousel indicator-position="outside" height="450px">
                <el-carousel-item v-for="(item,index) in sliders" :key="index">
                    <a :href="item.url"><img class="slider-image" :src="item.img_url"></a>
                </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
    export default {
        name:'IndexSlider',
        props:{
            sliders:{
                default:function () {
                    return [{url:'',img_url:''}]
                },
                type:Array
            }
        },
    }
</script>


<style>
    .slider-image{
        width: 100%;
        height: 100%;
    }

</style>