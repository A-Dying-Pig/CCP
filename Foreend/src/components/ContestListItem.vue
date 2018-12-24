<template>
    <div class="super-check-contest-item">
        <el-card shadow="hover">
            <div class="super-check-contest-item-image">
                <img :src="img_url" class="image">
            </div>

            <div class="super-check-contest-item-info">
                <div class="info-item"><span class="title">比赛标题:</span> <span class="content">{{title}}</span></div>
                <div class="info-item"><p class="title">比赛简介:</p> <p class="content">{{intro}}</p></div>
            </div>
            <div class="super-button">
                <el-button style="padding: 10px 5px" @click="$emit('new-contest-detail',contestid)">查看详情</el-button>
                <div class="super-button-text">
                    已报名<span class="super-button-number">{{enroll_number}}</span>队
                </div>
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
            intro:{
                default:'我爱你',
            },
            img_url:{
                default:require('../assets/img/logo.png'),
            },
            enroll_number:{
                default:0
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
        height:120px;
        width:120px;
        float: left;
        margin-bottom: 20px;
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
        margin-top: 5px;
        margin-bottom: 5px;
        word-break: break-all;
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
        margin-top: 20px;
    }

    .super-button-number{
        font-family: PingFang SC;
        color: deepskyblue;
        font-size: 15px;
    }
    .super-button-text{
        margin-top: 10px;
        font-family: PingFang SC;
        font-size: 12px;
    }
</style>