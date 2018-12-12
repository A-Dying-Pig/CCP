<template>
    <div class="ccp-footer">
        <div class="ccp-footer-col">

            <el-row :gutter="0">
                <el-col :span="4" :offset="2">
                    <FooterCol :footer_col="about_us"></FooterCol>
                </el-col>

                <el-col :span="4">
                    <FooterCol :footer_col="online_service"></FooterCol>
                </el-col>
            </el-row>


        </div>

        <div class="bottom-banner">本网站由CCP团队开发</div>

    </div>
</template>


<script>
    import FooterCol from './FooterCol'

    export default {
        data:function () {
            return {
                about_us:{
                    title:'关于我们',
                    content:[
                        {sub_title:'了解我们',href:'/about'},
                        {sub_title:'服务协议',href:'/service'}
                    ]
                },
                online_service:{
                    title:'在线客服',
                    content:[
                        {sub_title:'官方微信号:DingZheng',href:''},
                    ]
                }
            }
        },
        components:{
            FooterCol
        }
    }
</script>


<style>
    .ccp-footer{
        margin-top: 60px;
    }
    .ccp-footer-col{
        background: #383838;
        padding-top: 5px;
        padding-bottom: 30px;

    }

    .bottom-banner{
        background: #202020;
        color: #737373;
        padding-top:8px;
        padding-bottom: 8px;
        text-align: center;
        font-size: 14px;
        font-family: "PingFang SC";

    }

</style>