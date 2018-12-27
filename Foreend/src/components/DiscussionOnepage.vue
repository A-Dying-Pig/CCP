<template>
    <div>
        <div class="discussion-content">
            <div class="discussion-one-page-return-btn">
                <el-button @click="backtolist" type="text" icon="el-icon-back" >返回</el-button>
            </div>
            <div class="discussion-reply-title">
                内容
            </div>
            <el-card class="discussion-main">
                <div slot="header">
                    <div class="discussion-one-page-title">{{onedis.title}}</div>
                    <div class="discussion-one-page-author">作者:{{onedis.author}} </div>
                    <div class="discussion-one-page-time">时间:{{RealTime(onedis.issuetime)}} </div>
                </div>
                <div class="discussion-one-page-content">
                    {{onedis.content}}
                </div>
            </el-card>

        </div>


        <div class="discussion-reply">
            <div class="discussion-reply-title">
                评论
            </div>
            <div v-for="(item,index) in onedis.array" :key="index" class="discussion-per-reply">
                <DiscussionReply
                        :img_url="item.imgurl"
                        :username="item.username"
                        :time = "item.time"
                        :content = "item.content"
                        :floor="index + 1"
                >
                </DiscussionReply>
            </div>
        </div>

        <el-pagination v-if="onedis.total_page_num > 0"
                    layout="prev, pager, next"
                    :current-page="onedis.current_page_num"
                    :page-count="onedis.total_page_num"
                    @current-change="CurrentPageChange"
                    @prev-click="PagePrevious"
                    @next-click="PageNext"
                    class="discussion-page">
        </el-pagination>

        <div v-else class="no-reply-yet">
            还没有回复，快来抢沙发~
        </div>

        <div class="discussion-own-reply">
            <div class="discussion-reply-title">
                回复
            </div>
            <div class="discussion-reply-content">
                <el-input
                        type="textarea"
                        :rows="5"
                        placeholder="请输入回复内容"
                        v-model="the_reply">
                </el-input>
                <div class="discussion-reply-btn">
                    <el-button type="success" @click="ReplyClicked">回复</el-button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import DiscussionReply from './DiscussionReply.vue'
    //import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: "DiscussionOnepage",
        components:{
            DiscussionReply,
        },
        props:{
            showtype:{
                Type:Object,
                default:{show:0,discussionid:0}
            },
            onedis:{//detail of a discussion
                Type:Object,
                default:{
                }
            },
            contestid:{
                default:0
            }
        },
        data:function(){
            return{
                isshowList:this.showtype,
                the_reply:'',
            }
        },
        methods:{
            backtolist:function () {
                this.the_reply = '';
                this.isshowList.show = 0;
            },
            CurrentPageChange:function (cur_page) {
                console.log(cur_page);
                this.onedis.current_page_num = cur_page;
                let self = this;
                console.log(self.onedis.current_page_num);
                axios.post('/api/competition/discussion',{
                    contestid:self.contestid,
                    discussionid:self.showtype.discussionid,
                    pageNum:self.onedis.current_page_num,
                }).then(function (response) {
                    if(response.data.msg!==''){
                        self.$message({
                            message:response.data.msg,
                            type:'error'
                        });
                        return;
                    }
                    self.onedis.array.splice(0);
                    self.onedis = response.data;
                }).catch(function (error) {
                    console.log(error)
                    console.log('reply error!');
                    self.$message({
                        message:'获取帖子信息错误！',
                        type:'error'
                    });
                });
            },
            PagePrevious:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            PageNext:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
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
            ReplyClicked:function () {
                let vm = this;
                axios.post('/api/competition/discussionreply',
                    {
                        contestid: this.contestid,
                        discussionid: this.showtype.discussionid,
                        content: this.the_reply,
                    })
                    .then(response => {
                        if (response.data.msg !== '') {
                            vm.$message({
                                message: `回帖失败！${response.data.msg}`,
                                type: 'error'
                            });
                        }
                        else {
                            vm.the_reply = '';
                            vm.$message({
                                message: `回帖成功`,
                                type: 'success'
                            });
                            vm.CurrentPageChange(vm.onedis.current_page_num);
                        }
                    })
                    .catch(error => {
                        self.$message({
                            message: '回帖失败！',
                            type: 'error'
                        });
                    });
            }
        }
    }
</script>

<style>
.discussion-one-page-title{
    font-weight: bold;
    font-size: 28px;
}

.discussion-one-page-return-btn{
    margin-left: 10px;
}

.discussion-reply-title{
    font-size: 25px;
    margin-top:20px;
    margin-left:10px;
    margin-bottom: 20px;
}

.discussion-per-reply{
    margin-top: 10px;
    margin-bottom: 10px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}
.discussion-page{
    text-align: center;
    margin-top: 40px;
}

.discussion-own-reply{
    margin-top: 20px;
}

.discussion-one-page-author{
    color:gray;
    font-size: 14px;
    margin-top:5px;
}

.discussion-one-page-time{
    color:gray;
    font-size: 14px;
    margin-top:5px;
}
.discussion-main{
    margin-left: 10px;
}

.discussion-reply-content{
    margin-left: 10px;
}

.discussion-reply-btn{
    margin-top: 20px;
    margin-bottom: 20px;
    text-align: center;
}

.no-reply-yet{
    margin-top: 20px;
    color: gray;
    margin-bottom: 20px;
    text-align: center;

}

</style>