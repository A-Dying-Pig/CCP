<template>
  <div id="app">
    <el-container>
      <el-header height="100px" class="header">
        <div><NavigationBar :username="musername"></NavigationBar></div>
      </el-header>
    </el-container>

    <el-container>
      <el-main>
          <el-tabs v-model="activeName">
            <el-tab-pane label="审核比赛" name="1">

              <div v-if="contest_switch === 0" class="contest_list">
                <el-row :gutter="0" v-for="(item,index) in contest_list.array" :key="index">
                  <el-col :span="12" :offset="6" >
                    <SuperCheckContestItem
                          :contestid="item.contestid"
                          :holders="item.holders"
                          :sponsors="item.sponsors"
                          :img_url="item.img_url"
                          :title="item.title"
                          @new-contest-detail="ShowContestDetail"></SuperCheckContestItem>
                  </el-col>
                </el-row>

                <el-pagination
                        layout="prev, pager, next"
                        :current-page="contest_list.current_page_num"
                        :page-count="contest_list.total_page_num"
                        @current-change="CurrentPageChange"
                        @prev-click="PagePrevious"
                        @next-click="PageNext"
                        class="profile-page">
                </el-pagination>
              </div>

              <div v-else-if="contest_switch===1" class="contest_detail">
                <el-row :gutter="0">
                  <el-col :span="12" :offset="6" >
                    <div>
                      <el-button type="text" icon="el-icon-back" @click="ContestBackClick" ><span class="super-back-btn">返回</span></el-button>
                    </div>
                  </el-col>
                </el-row>

                <el-row :gutter="0">
                  <el-col :span="12" :offset="6" >
                    <el-card shadow="hover" class="contest-card">
                    <div slot="header" class="detail-header">
                      比赛基本信息
                    </div>
                    <div class="basic-info">
                      <div class="info-item"><span class="title">比赛名称:</span> <span class="content">{{contest_detail.basicinfo.name}}</span></div>
                      <div class="info-item"><span class="title">举办方:</span> <span v-for="(item,index) in contest_detail.basicinfo.holders" :key="index" class="content">{{item}}</span></div>
                      <div class="info-item"><span class="title">承办方:</span> <span v-for="(item,index) in contest_detail.basicinfo.sponsors" :key="index" class="content">{{item}}</span></div>
                      <div class="info-item"><span class="title">比赛类型:</span> <span class="content">{{contest_detail.basicinfo.comtype}}</span></div>
                      <div class="info-item"><span class="title">比赛详情:</span> <br>
                        <p class="content">{{contest_detail.basicinfo.details}}</p></div>
                    </div>
                  </el-card>
                  </el-col>
                </el-row>

                <el-row :gutter="0">
                  <el-col :span="12" :offset="6" >
                    <el-card shadow="hover" class="contest-card">
                      <div slot="header" class="detail-header">
                        比赛报名信息
                      </div>
                      <div class="signup-info">
                        <div class="info-item"><span class="title">报名开始时间:</span> <span class="content">{{contest_detail.signupinfo.time[0]}}</span></div>
                        <div class="info-item"><span class="title">报名结束时间:</span> <span class="content">{{contest_detail.signupinfo.time[1]}}</span></div>
                        <div class="info-item">
                          <span class="title">比赛类型:</span>
                          <span v-if="contest_detail.signupinfo.mode === 1" class="content">个人赛</span>
                          <span v-else-if="contest_detail.signupinfo.mode === 0" class="content">组队赛</span>
                        </div>
                        <div class="info-item"><span class="title">参赛选手填写信息:</span> <span v-for="(item,index) in contest_detail.signupinfo.person" :key="index" class="content">{{item}}</span></div>
                        <div class="info-item"><span class="title">参赛队伍填写信息:</span> <span v-for="(item,index) in contest_detail.signupinfo.group" :key="index" class="content">{{item}}</span></div>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>

                <el-row :gutter="0">
                  <el-col :span="12" :offset="6" >
                    <el-card shadow="hover" class="contest-card">
                      <div slot="header" class="detail-header">
                        阶段比赛信息
                      </div>
                      <div v-for="(item,index) in contest_detail.stageinfo" :key="index" class="stage-info">
                        <div class="info-item"><span class="title">阶段比赛名称:</span> <span class="content">{{item.name}}</span></div>
                        <div class="info-item"><span class="title">阶段比赛详情:</span> <span class="content">{{item.details}}</span></div>
                        <div class="info-item"><span class="title">阶段比赛开始日期:</span> <span class="content">{{RealTime(item.stageTimeBegin)}}</span></div>
                        <div class="info-item"><span class="title">阶段比赛提交截止日期:</span> <span class="content">{{RealTime(item.handTimeEnd)}}</span></div>
                        <div class="info-item"><span class="title">阶段比赛打分截止日期:</span> <span class="content">{{RealTime(item.evaluationTimeEnd)}}</span></div>
                        <div class="info-item"><span class="title">打分方式:</span> <span class="content">{{item.mode}}</span></div>
                        <hr>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>

                <el-row :gutter="0">
                  <div class="super-btn">
                    <el-button style="padding: 10px 5px" type="success" @click="CheckPass(1)">审核通过</el-button>
                    <el-button style="padding: 10px 5px" type="danger" @click="CheckPass(0)">审核未通过</el-button>
                  </div>
                </el-row>

              </div>
            </el-tab-pane>

            <el-tab-pane label="设置首页热门比赛和轮播图" name="2">
              <IndexInfo></IndexInfo>
            </el-tab-pane>
          </el-tabs>
      </el-main>

      <el-container>
        <el-footer>
          <CCPFooter></CCPFooter>
        </el-footer>
      </el-container>

    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import SuperCheckContestItem from '../../components/SuperCheckContestItem'
    import IndexInfo from '../../components/IndexInfo'
    import CCPFooter from '../../components/CCPFooter'
    //import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: 'app',
        props:{
            musername:{
                default:'',
                type:String,
            }
        },
        data() {
            return {
                activeName:'1',
                contest_list:{
                    current_page_num:1,
                    total_page_num:1,
                    array: [
                    ]
                },
                contest_switch:0, // 0 for contest list; 1 for detail information
                contest_detail_id:0,
                contest_detail:{
                }
            }
        },
        components: {
            IndexInfo,
            NavigationBar,
            SuperCheckContestItem,
            CCPFooter
        },
        mounted:function () {
            axios.post('/api/super/contests',{pageNum:1})
                .then(response=>{
                        this.contest_list = response.data;
                });
        },

        methods:{
            CurrentPageChange:function (cur_page) {
                axios.post('/api/super/contests',{pageNum:cur_page})
                    .then(response=>{
                        this.contest_list = response.data;
                    })
            },
            PagePrevious:function (cur_page) {
                axios.post('/api/super/contests',{pageNum:cur_page})
                    .then(response=>{
                        this.contest_list = response.data;
                    })
            },
            PageNext:function (cur_page) {
                axios.post('/api/super/contests',{pageNum:cur_page})
                    .then(response=>{
                        this.contest_list = response.data;
                    })
            },
            ShowContestDetail:function (id) {
                this.contest_detail_id = id;
                axios.post('/api/super/detail',{contestid:id})
                    .then(response=>{
                        this.contest_detail = response.data;
                        this.contest_switch = 1;
                    });
                this.contest_switch = 1;
            },
            ContestBackClick:function () {
                this.contest_switch = 0;
            },
            CheckPass:function ( cur_pass ) {
                let vm = this;
                axios.post('/api/super/submit',{ contestid:this.contest_detail_id,pass:cur_pass})
                    .then(response=>{
                        if(response.data.msg === ''){
                            vm.$message({
                                message: '操作成功!',
                                type: 'success'
                            });
                            axios.post('/api/super/contests',{pageNum:1})
                                .then(response=>{
                                    this.contest_list = response.data;
                                });
                        }
                        else{
                            vm.$message({
                                message: `操作失败! ${response.data}`,
                                type: 'error'
                            });
                        }
                        vm.contest_switch = 0;
                    });
                this.contest_switch = 0;
            },
            RealTime:function (timestamp) {
                let now = new Date(timestamp),
                    y = now.getFullYear(),
                    m = now.getMonth() + 1,
                    d = now.getDate();
                let str = y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d) + " " + now.toTimeString().substr(0, 8);
                //console.log(str);
                return str;
            }
        }
    }
</script>

<style>
  .profile-page{
    margin-top: 60px;
    text-align: center;
  }

  .el-row{
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .detail-header{
    font-weight: bold;
    font-size: 25px;
  }

  .title{
    font-weight: bold;
    font-family: PingFang SC;
  }

  .content{
    color: gray;
    padding-left: 20px;
    white-space:normal;
  }

  .info-item{
    margin-top: 5px;
    margin-bottom: 5px;
    word-wrap: break-word;
  }

  .stage-info{
    margin-bottom: 20px;
  }

 .contest-card{
   margin-top: 20px;
 }

  .super-btn{
    text-align: center;
  }

  .super-back-btn{
    font-size: 18px;
  }

</style>