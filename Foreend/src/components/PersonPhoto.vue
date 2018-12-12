<template>
    <div class="person-center-photo-div">
        <div class="person-center-photo-title">个人头像</div>
        <div>
            <img :src="img_url" class = 'person-center-photo'>
        </div>
    </div>
</template>


<script>
    export default {
        props:{
            img_url:{
                type:String,
                default:require("../assets/img/logo.png"),
            }
        }
    }
</script>

<style>
    .person-center-photo-title{
        padding-top: 30px;
        font-size: 16px;
        font-family: PingFang SC;
        text-align: center;
    }

    .person-center-photo{
        width: 80%;
        border: 1px solid lightgray;
        margin-left: 10%;
        margin-top: 20px;
        margin-bottom: 60px;
        height: 200px;

    }
    .person-center-photo-div{
        width: 99.5%;
        border-right: 1px solid lightgray;
    }

</style>