<template>
    <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <a :href="competition_profile.url"><img :src="competition_profile.img" class="card_image"></a>
        <div style="padding: 14px;" class="card_text">
            <div class="card_title">{{competition_profile.title}}</div>
            <div class="card_intro"> {{competition_profile.intro}}</div>
        </div>
    </el-card>
</template>

<script>
    export default {
        props:{
            competition_profile:{
                type:Object,
                default:function () {
                    return {url:'',img:'',title:'',intro:''}
                }
            }
        },
        data() {
            return {
                currentDate: new Date()
            };
        }
    }
</script>

<style>
    .card_image {
        width: 100%;
        height:200px;
        display: block;
    }

    .card_title{
        overflow: hidden;
        white-space: nowrap;
        word-break: break-all;
        text-overflow:ellipsis;
    }
    .card_intro{
        height: 60px;
        color:gray;
        font-size: 14px;
        overflow: hidden;
        white-space:normal;
        word-break: break-all;
        text-overflow:ellipsis;
    }
</style>