<template>
    <div class="discuss-reply">
        <el-card class="box-card">
            <div class="title">
                <div class="user-image">
                    <img :src="img_url" class="the-image">
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
            img_url:{
                default:require('../assets/img/logo.png')
            },
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
            }
        },
        methods:{
            RealTime:function (timestamp) {
                let now = new Date();
                let then = new Date(timestamp);
                //year
                if(then.getFullYear()!==now.getFullYear()){
                    return now.getFullYear()-then.getFullYear()+'年前';
                }
                //month
                else if(then.getMonth()!==now.getMonth()){
                    return now.getMonth()-then.getMonth()+'月前';
                }
                //day
                else if(then.getDay()!==now.getDay()){
                    return now.getDay()-then.getDay()+'天前';
                }
                else {
                    let hour =then.getHours()+'';
                    let minite = then.getMinutes()+'';
                    if(then.getMinutes()<10){
                        minite = '0'+minite;
                    }
                    return hour+':'+minite;
                }
            },
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
    text-align: left;
}
.user-other{
    color:gray;
    font-size:12px;
    margin-top:5px;
}
.content{
    margin-top: 60px;
    margin-left:100px;
    word-wrap: break-word;

}
</style>