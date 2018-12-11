<template>
    <div>
        <p>{{ onedis.title }}</p>
        <el-button @click="backtolist">返回</el-button>
    </div>
</template>

<script>

    export default {
        name: "DiscussionOnepage",
        props:{
            showtype:{
                Type:Object,
                default:{show:0}
            },
            onedis:{//detail of a discussion
                Type:Object,
                default:{}
            }
        },
        data:function(){
            return{
                isshowList:this.showtype,
            }
        },
        methods:{
            backtolist:function () {
                this.isshowList.show = 0;
            }
        }
    }
</script>

<style scoped>
</style>