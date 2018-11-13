<template>
    <div class="index-slider" >
        <el-carousel indicator-position="outside">
                <el-carousel-item v-for="(item,index) in sliders" :key="index">
                    <a :href="item.url"><img class="slider-image" :src="item.img_url"></a>
                </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
    //sliders: [ {url: ,img_url: }]
    export default {
        name:'IndexSlider',
        props:{
            sliders:{
                default:function () {
                    return [{url:'www.baidu.com',img_url:require('../assets/1.png')},
                        {url:'www.baidu.com',img_url:require('../assets/2.png')}]
                },
                type:Array
            }
        },
    }
</script>


<style>
    .slider-image{
        width: 600px;
        height: 300px;
    }

    .index-slider{
        width: 600px;
        height: 150px;
    }
</style>