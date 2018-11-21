<template>
    <div class="super-check-contest-item">
        <el-card shadow="hover">
            <div class="super-check-contest-item-image">
                <img :src="img_url" class="image">
            </div>

            <div class="super-check-contest-item-info">
                <div class="info-item"><span class="title">比赛id:</span> <span class="content">{{contestid}}</span></div>
                <div class="info-item"><span class="title">比赛标题:</span> <span class="content">{{title}}</span></div>
                <div class="info-item"><span class="title">举办方:</span> <span v-for="(item,index) in holders" :key="index" class="content">{{item}}</span></div>
                <div class="info-item"><span class="title">承办方:</span> <span v-for="(item,index) in sponsors" :key="index" class="content">{{item}}</span></div>
            </div>
            <div class="super-button">
                <el-button style="padding: 10px 5px" @click="$emit('new-contest-detail',contestid)">查看详情</el-button>
            </div>
        </el-card>

    </div>
</template>

<script>
    export default{
        props:{
            contestid:{
                default:0,
            },
            title:{
                default:'我不想写了比赛了',
            },
            holders:{
                default:['可爱的林克','哥布林'],
            },
            sponsors:{
                default:["lyr","233"],
            },
            img_url:{
                default:require('../assets/img/logo.png'),
            }
        },
        data:function () {
            return{
            }

        }
    }

</script>

<style>
    .super-check-contest-item-image{
        height:130px;
        width:130px;
        float: left;
    }
    .image{
        height:130px;
        width:130px;
    }
    .super-check-contest-item-info{
        padding-left: 40px;
        float: left;
        width: 50%;
    }
    .info-item{
        overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    .title{
        font-weight: bold;
        font-family: PingFang SC;
    }
    .content{
        color: gray;
        padding-left: 20px;
    }
    .super-button{
        float: right;
        margin-top: 30px;
    }

</style>