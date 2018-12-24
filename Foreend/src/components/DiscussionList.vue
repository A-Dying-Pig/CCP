<template>
<div>
    <el-row :gutter="24">
        <el-col :span="4">
            <el-button @click="towrite" type="primary">发表帖子</el-button>
        </el-col>
    </el-row>
    <el-row type="flex" justify="center">
        <el-col :span="24">
    <el-table :data="disdata" :show-header="false" @row-click="toone">
        <el-table-column min-width="6" >
            <template slot-scope="scope">
                <div>
                    <p class="discussiontitle">{{ scope.row.title }}</p>
                    <p class="discussionlight">{{ scope.row.author }},  {{ scope.row.fmissuetime }}  |  最新回复:  {{ scope.row.fmlasttime }}</p>
                </div>
            </template>
        </el-table-column>
        <el-table-column min-width="1" >
            <template slot-scope="scope">
                <div>
                    <p class="discussiontitle">{{ scope.row.replynum }}</p>
                    <p class="discussionlight">回复</p>
                </div>
            </template>
        </el-table-column>
        <el-table-column min-width="1" >
            <template slot-scope="scope">
                <div>
                    <p class="discussiontitle">{{ scope.row.viewnum }}</p>
                    <p class="discussionlight">浏览</p>
                </div>
            </template>
        </el-table-column>
    </el-table>
        </el-col>
    </el-row>
    <el-row type="flex" justify="center">
        <el-col :span="12">
    <el-pagination
            @current-change="handleCurrentChange"
            :current-page.sync="current_page_num"
            :page-count="total_page_num"
            layout="prev, pager, next, jumper">
    </el-pagination>
        </el-col>
    </el-row>
</div>
</template>

<script>
    //import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "DiscussionList",
        props:{
            showtype:{
                Type:Object,
                default:{show:0,discussionid:0}
            },
            current_page_num:{
                Type:Number,
                default:1
            },
            total_page_num:{
                Type:Number,
                default:10
            },
            disdatap:{
                Type:Array,
                default:[]
            },
            contestid:{
                Type:Number,
                default:-1
            }
        },
        data:function(){
          return{
              isshowList:this.showtype,
              disdata:this.disdatap
          }
        },
        methods:{
            toone:function (row, event, column) {
                let self = this;
                this.isshowList.show = 1;
                this.showtype.discussionid = row.discussionid;
                //get one discussion
                axios.post('/api/competition/discussion',{
                    contestid:self.contestid,
                    discussionid:row.discussionid,
                    pageNum:1
                }).then(function (response) {
                    if(response.data.msg!==''){
                        self.$message({
                            message:response.data.msg,
                            type:'error'
                        });
                        return
                    }
                    //self.onedis = response.data;
                    self.$emit('new-onedis',response.data);
                }).catch(function (error) {
                    console.log(error)
                    self.$message({
                        message:'获取帖子信息错误！',
                        type:'error'
                    });
                });
            },
            towrite:function(){
                this.isshowList.show = 2;
            },
            handleCurrentChange:function (pagenum) {
                //console.log(pagenum);
                this.getdata(pagenum);
            },
            timeformat:function (stamp) {
                let now = new Date();
                let then = new Date(stamp);
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
            getdata:function (pagenum) {
                let self = this;
                axios.post('/api/competition/discussionlist',{
                    pageNum:pagenum,
                    contestid:self.contestid
                }).then(function (response) {
                    self.current_page_num = 1;
                    self.total_page_num = 10;
                    self.disdata = [];
                    if(response.data.msg !== ''){
                        self.$message({
                            message:response.data.msg,
                            type:'success'
                        });
                        return
                    }
                    self.current_page_num = response.data.current_page_num;
                    self.total_page_num = response.data.total_page_num;
                    self.disdata = response.data.array;
                    for(let onedata of self.disdata){
                        onedata.fmissuetime = self.timeformat(onedata.issuetime);
                        onedata.fmlasttime = self.timeformat(onedata.lasttime);
                    }
                    console.log(self.disdata)
                }).catch(function (error) {
                    self.$message({
                        message:'获取讨论区列表失败！',
                        type:'error'
                    });
                });
            }
        },
        created:function () {
            let self = this;
            self.disdata = [
            ];
            self.getdata(1);
        }
    }
</script>

<style scoped>
    .discussiontitle{
        font-size: 15px;
        font-weight: 700;
        font-family: 微软雅黑;
        color: black;
    }
    .discussionlight{
        font-size: 12px;
        font-weight: 700;
        font-family: 微软雅黑;
        color: gray;
    }
</style>