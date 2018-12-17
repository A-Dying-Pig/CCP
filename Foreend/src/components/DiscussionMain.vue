<template>
    <div>
        <DiscussionList v-show="showtype.show === 0" :contestid="contestid" :showtype="showtype" :current_page_num="current_page_num" :total_page_num="total_page_num" :disdatap="disdata" :width="width" :onedis="onedis"
        @new-onedis="update_onedis"></DiscussionList>
        <DiscussionOnepage v-show="showtype.show === 1" :showtype="showtype" :contestid="contestid" :onedis="onedis"></DiscussionOnepage>
        <DiscussionWrite v-show="showtype.show === 2" :showtype="showtype" :contestid="contestid"></DiscussionWrite>
    </div>
</template>

<script>
    import DiscussionList from './DiscussionList'
    import DiscussionOnepage from './DiscussionOnepage'
    import DiscussionWrite from './DiscussionWrite'
    export default {
        name: "DiscussionMain",
        components:{DiscussionWrite, DiscussionList, DiscussionOnepage},
        props:{
            contestid:{
                Type:Number,
                default:-1
            },
            width:{
                Type:Number,
                default:0
            }
        },
        data:function () {
            return{
                showtype:{
                    show:0,
                    discussionid:0,
                },
                current_page_num:1,
                total_page_num:10,
                disdata:[],
                onedis:{
                        current_page_num:1,
                        total_page_num:5,
                        title: '测试标题',
                        content:"I am a good student. My name is Leiyiran",
                        author:'你好我叫雷怡然',
                        issuetime:1234567891234,
                        array:[
                            {
                                imgurl:require('../assets/img/logo.png'),
                                username:'Flying Donut',
                                content:"You are right",
                                time:1234567891011,
                            },
                            {
                                imgurl:require('../assets/img/logo.png'),
                                username:'Flying Donut2',
                                content:"You are right2",
                                time:3234567891011,
                            }
                        ]
                }
            }
        },
        created:function () {

        },
        mounted:function () {
            let self = this;
        },
        methods:{
            update_onedis:function (data) {
                this.onedis = data;
            }

        }
    }
</script>

<style scoped>

</style>