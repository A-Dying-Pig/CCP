<template>
    <div class="footer-col">
        <div class="footer-col-title">{{footer_col.title}}</div>
        <hr class="footer-col-spliter" align="left">
        <div v-for="(item,index) in footer_col.content" :key="index" class="footer-col-sub">
            <a v-if="item.href!==''" :href="item.href" class="footer-col-sub-content-link">{{item.sub_title}}</a>
            <span v-else class="footer-col-sub-content"> {{item.sub_title}}</span>
        </div>
    </div>
</template>

<script>
    export default {
        props:{
            footer_col:{
                default:{
                    title:'关于我们',
                    content:[
                        {sub_title:'了解我们',href:'/about'},
                        {sub_title:'服务协议',href:'/service'},
                    ]
                }
            }
        }
    }

</script>

<style>

    .footer-col-spliter{
        border-color: lightgray;
        border-width: 1px;
        width: 50%;
        padding-top: 10px;
        border-bottom-width: 0px;
        border-left-width: 0px;
        border-right-width: 0px;

    }
    .footer-col-title{
        font-size: 25px;
        font-family: "PingFang SC";
        color:white;
        text-align: left;
        padding-top: 25px;
        margin-bottom: 15px;
    }

    .footer-col-sub{
        text-align: left;
        margin-top:10px;
        margin-bottom: 10px;
    }
    .footer-col-sub-content-link{
        text-decoration: none;
        color: lightgray;
    }
    .footer-col-sub-content-link:hover{
        text-decoration: none;
        color: dodgerblue;
    }

    .footer-col-sub-content{
        text-decoration: none;
        color: lightgray;
    }


</style>