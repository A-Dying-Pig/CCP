<template>
    <div>
        <DiscussionList v-show="showtype.show === 0" :contestid="contestid" :showtype="showtype" :current_page_num="current_page_num" :total_page_num="total_page_num" :disdatap="disdata" :width="width" :onedis="onedis"
        @new-onedis="update_onedis"></DiscussionList>
        <DiscussionOnepage v-show="showtype.show === 1" :showtype="showtype" :contestid="contestid" :onedis="onedis"></DiscussionOnepage>
        <DiscussionWrite v-show="showtype.show === 2" :showtype="showtype" :contestid="contestid"></DiscussionWrite>
    </div>
</template>

<script>
    import DiscussionList from './DiscussionList.vue'
    import DiscussionOnepage from './DiscussionOnepage.vue'
    import DiscussionWrite from './DiscussionWrite.vue'
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