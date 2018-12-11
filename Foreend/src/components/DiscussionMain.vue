<template>
    <div>
        <DiscussionList v-show="showtype.show === 0" :contestid="contestid" :showtype="showtype" :current_page_num="current_page_num" :total_page_num="total_page_num" :disdatap="disdata" :width="width" :onedis="onedis"></DiscussionList>
        <DiscussionOnepage v-show="showtype.show === 1" :showtype="showtype" :onedis="onedis"></DiscussionOnepage>
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
                    show:0
                },
                current_page_num:1,
                total_page_num:10,
                disdata:[],
                onedis:{
                    msg:'',
                    current_page_num:0,
                    total_page_num:0,
                    title:'',
                    content:'',
                    author:'',
                    issuetime:0,
                    array:[]
                }
            }
        },
        methods:{

        },
        created:function () {

        },
        mounted:function () {
            let self = this;
        }
    }
</script>

<style scoped>

</style>