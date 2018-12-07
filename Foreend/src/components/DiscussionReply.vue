<template>
    <div class="discuss-reply">
        <el-card class="box-card">
            <div class="title">
                <div class="user-image">
                    <img src="../assets/1.png" class="the-image">
                </div>
                <div class="user-text">
                    <div class="user-name">
                        {{username}}
                    </div>
                    <div class="user-other">
                        {{floor}}楼 {{RealTime(time)}}
                    </div>
                </div>
            </div>
            <div class="content">
                {{content}}
            </div>
        </el-card>
    </div>

</template>


<script>
    export default{
        props:{
            //img_url:{
            //    default:require('../assets/1.png')
            //},
            username:{
                default:'leiyiran',
            },
            floor:{
                default:0
            },
            time:{
                default:1231231231231
            },
            content:{
                default:'hello,world'
            }
        },
        data:function () {
            return {
                img_url:{
                    default:require('../assets/1.png')
                },
            }
        },
        methods:{
            RealTime:function (timestamp) {
                let now = new Date(timestamp),
                    y = now.getFullYear(),
                    m = now.getMonth() + 1,
                    d = now.getDate();
                let str = y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d) + " " + now.toTimeString().substr(0, 8);
                return str;
            }
        }
    }
</script>


<style>
.user-image{
    float: left;
}
.the-image{
    width:60px;
    height:60px;
    border-radius:60px;
    border: 1px solid lightgray;
}
.user-text{
    margin-left: 40px;
    float: left;
}
.user-name{
    font-weight:bold;
    font-size:20px;
}
.user-other{
    color:gray;
    font-size:12px;
    margin-top:5px;
}
.content{
    margin-top: 80px;
    margin-left:100px;
}
</style>