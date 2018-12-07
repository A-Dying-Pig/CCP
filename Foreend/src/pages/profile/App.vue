<template>
  <div id="app">
    <el-container>
      <el-header height="100px" class="header">
        <div><NavigationBar :username="musername"></NavigationBar></div>
      </el-header>
    </el-container>

    <el-container>
      <el-aside width="250px">
        <PersonPhoto :img_url="img_url"></PersonPhoto>

        <div class="person-center-aside-menu">
        <el-menu :default-active="which_menu" @select="UpdateMenu">
          <el-menu-item index="1">
            <i class="el-icon-document"></i>
            <span slot="title">相关比赛</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-setting"></i>
            <span slot="title">个人信息设置</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-bell"></i>
            <span slot="title">消息列表</span>
          </el-menu-item>
          </el-menu>
        </div>
      </el-aside>


      <el-main>
        <!--competition-->
        <div v-show="which_menu === '1'">
          <el-tabs v-model="activeName">
            <el-tab-pane label="我参加的比赛" name="1">
              <el-table :data="competition.participated_competition" style="width: 100%">
                <el-table-column
                        prop="title"
                        label="参加的比赛"
                        min-width="4"
                        >
                </el-table-column>
                <el-table-column
                        label="操作"
                        min-width="2"
                        >
                  <template slot-scope="scope">
                    <a :href="competition.participated_competition[scope.$index].url" class="person-table-btn el-button">查看详情</a>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="我创建的比赛" name="2">

              <div v-show="send_message_switch===0"  class="created-contests-table">
              <el-table :data="competition.created_competition" style="width: 100%">
                <el-table-column
                        prop="title"
                        label="创建的比赛"
                        min-width="4"
                >
                </el-table-column>
                <el-table-column
                        label="操作"
                        min-width="2"
                >
                  <template slot-scope="scope">
                    <a :href="competition.created_competition[scope.$index].url" class="person-table-btn el-button">查看详情</a>
                    <el-button type="info" @click="SendMessageClicked(competition.created_competition[scope.$index].id,scope.$index)">发送消息</el-button>
                  </template>
                </el-table-column>
              </el-table>
              </div>

              <div v-show="send_message_switch===1" class="created-contests-send-message">
                <div class="send-message-btn">
                  <el-button type="text" icon="el-icon-back" @click="SendMessageBack">返回</el-button>
                </div>

                <div class="message-target">
                  <div>请选择对象</div>
                  <el-cascader
                          expand-trigger="hover"
                          :options="send_message_menu"
                          v-model="send_message_target"
                  >
                  </el-cascader>
                </div>

                <div class="send-message-select">
                  <el-radio v-model="send_message_type" label=0>全部选手</el-radio>
                  <el-radio v-model="send_message_type" label=1>当前阶段赛晋级选手</el-radio>
                  <el-radio v-model="send_message_type" label=-1>当前阶段赛淘汰选手</el-radio>
                </div>

                <div class="send-message-input">
                  <div class="send-message-input-title">消息标题
                    <el-input
                          type="textarea"
                          autosize
                          placeholder="请输入标题"
                          v-model="send_message_title">
                    </el-input>
                  </div>
                  <div class="send-message-input-content">消息内容
                    <el-input
                          type="textarea"
                          :autosize="{ minRows:8,maxRows: 10}"
                          placeholder="请输入内容"
                          v-model="send_message_content">
                    </el-input>
                  </div>
                </div>

                <div class="send-message-btn">
                  <el-button type="success" @click="SendMessageSubmit">发布</el-button></div>
                </div>

            </el-tab-pane>
            <el-tab-pane label="我参评的比赛" name="3">
              <el-table :data="competition.rated_competition" style="width: 100%">
                <el-table-column
                        prop="title"
                        label="参评的比赛"
                        min-width="4"
                >
                </el-table-column>
                <el-table-column
                        label="操作"
                        min-width="2"
                >
                  <template slot-scope="scope">
                    <a :href="competition.rated_competition[scope.$index].url" class="person-table-btn el-button">查看详情</a>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!--pesonal info settings -->
        <div v-show="which_menu === '2'">
          <el-card >
            <div slot="header" class="clearfix">
              <span>现存信息</span>
              <el-button v-if="info_saved===true" style="float: right;padding: 5px 2px" type="primary" @click="ChangeInfo">修改</el-button>
              <el-button v-else style="float: right;padding: 5px 2px" type="success" @click="SaveInfo">保存</el-button>
            </div>

            <div class="text item">
              <div v-show="info_saved === true">
                <span class="person-info-card-title">所在大学</span>
                <span class="person-info-card-value">{{person.university}}</span>
              </div>
              <UniversityPicker v-show="info_saved === false" @new-university="UpdateUniversity"></UniversityPicker>
            </div>
            <hr>
            <div class="text item">
              <div v-show="info_saved === true">
                <span class="person-info-card-title">所在地区</span>
                <span class="person-info-card-value">{{person.region.province}} {{person.region.city}}</span>
              </div>
              <RegionPicker v-show="info_saved === false" @new-region="UpdateRegion"></RegionPicker>
            </div>
          </el-card>
        </div>

        <!--message list -->
        <div v-show="which_menu === '3'">

          <div v-if="message_switch === 0" class="message-list">
            <el-table :data="message_list.array" style="width: 100%">
          <el-table-column
                  prop="messageId"
                  label="序号"
                  min-width="1"
          >
          </el-table-column>
          <el-table-column
                  prop="context"
                  label="简介"
                  min-width="6"
          >
          </el-table-column>

            <el-table-column
                    label="状态"
                    min-width="2"
            >
              <template slot-scope="scope">
                <el-button v-if="message_list.array[scope.$index].read === 0" style="padding: 5px 2px" type='danger' @click="MessageClick(scope.$index)">未读</el-button>
                <el-button v-else-if="message_list.array[scope.$index].read === 1" style="padding: 5px 2px" type="success" @click="MessageClick(scope.$index)">已读</el-button>
              </template>
            </el-table-column>

            </el-table>

            <el-pagination
                  layout="prev, pager, next"
                  :current-page="message_list.current_page_num"
                  :page-count="message_list.total_page_num"
                  @current-change="CurrentPageChange"
                  @prev-click="PagePrevious"
                  @next-click="PageNext"
                  class="profile-page">
            </el-pagination>
          </div>

          <div v-if="message_switch === 1" class="message-detail">
              <div>
                <el-button type="text" icon="el-icon-back" @click="MessageBackClick">返回</el-button>
              </div>
              <div class="message-detail-title">
                <h2>{{message_detail.title}}</h2>
              </div>
              <hr>
              <div class="message-detail-content">
                {{message_detail.content}}
              </div>
          </div>

        </div>

      </el-main>

    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import PersonPhoto from '../../components/PersonPhoto'
    import RegionPicker from '../../components/RegionPicker'
    import UniversityPicker from '../../components/UniversityPicker'
    import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        //'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: 'app',
        props:{
            which_menu:{ //1 competitions; 2 settings; 3 message lists
                default:'1',
            },
            musername:{
                default:'',
                type:String,
            }
        },
        data() {
            return{
                img_url:require('../../assets/img/logo.png'),
                activeName: '1',
                competition:{
                    participated_competition:[],
                    created_competition:[],
                    rated_competition:[],
                },
                person:{
                    university:'',
                    region:{
                        province:'',
                        city:''
                    }
                },
                new_person:{
                    university:'',
                    region:{
                        province:'',
                        city:''
                    }
                },
                info_saved:true,
                //message list
                message_list:{
                    current_page_num:1,
                    total_page_num:1,
                    array:[
                        {messageId:1,context:'报名成功',read:0},
                        {messageId:2,context:'感谢您成为CCP网站用户',read:1}
                    ],
                },
                message_detail:{
                    title:'CCP网站滑水大赛报名成功',
                    content:'带上你的泳衣在炎日的冬季一起滑水吧!',
                },
                message_detail_index:0,
                message_switch:0, //0 for message list,1 for message detail
                send_message_switch:0,
                send_message_contest:-1,
                send_message_target:[],
                send_message_menu:[
                    {value:0,label:'所有选手'},
                    {value:-1,label:'赛区',children: [{value:1,label:'上海'}]}
                ],
                send_message_title:'',
                send_message_content:'',
                send_message_type:-1,
            }
        },
        components: {
            NavigationBar,
            PersonPhoto,
            RegionPicker,
            UniversityPicker
        },
        mounted:function () {
            axios.post('/api/user/profile')
                .then(response=>{
                  this.img_url = response.data.img_url;
                  this.competition = response.data.competition;
                  this.person = response.data.person;
                  this.new_person = this.person;
                });
            axios.post('/api/message/getall',{pageNum:this.message_list.current_page_num})
                .then(response=>{
                    this.message_list = response.data;
                });
        },
        methods:{
            UpdateMenu:function (index) {
                this.which_menu = index;
            },
            ChangeInfo:function () {
                this.info_saved = false;
            },
            SaveInfo:function () {
                axios.post('/api/user/modify',this.new_person);
                this.person = this.new_person;
                this.info_saved = true;
            },
            UpdateRegion:function (value) {
                this.new_person.region.province = value.province.value;
                this.new_person.region.city = value.city.value;
            },
            UpdateUniversity:function (data) {
                this.new_person.university = data;
            },
            CurrentPageChange:function (cur_page) {
                axios.post('/api/message/getall',{pageNum:cur_page})
                    .then(response=>{
                        this.message_list = response.data;
                    })
            },
            PagePrevious:function (cur_page) {
                axios.post('/api/message/getall',{pageNum:cur_page})
                    .then(response=>{
                        this.message_list = response.data;
                    })
            },
            PageNext:function (cur_page) {
                axios.post('/api/message/getall',{pageNum:cur_page})
                    .then(response=>{
                        this.message_list = response.data;
                    })
            },
            MessageClick:function(index){
                this.message_detail_index = index;
                axios.post('/api/message/detail',{messageId:this.message_list.array[index].messageId})
                    .then(response=>{
                        this.message_detail = response.data;
                        this.message_list.array[index].read = 1;
                        this.message_switch = 1;
                    });
                //Going to delete
                this.message_list.array[index].read = 1;
                this.message_switch = 1;
            },
            MessageBackClick:function () {
                this.message_switch = 0;
            },
            SendMessageClicked:function (contest_id,index) {
                this.send_message_contest = contest_id;
                /*
                let len = this.competition.created_competition[index].list.length;
                if (len !== 0){
                    this.$set(this.send_message_menu, 1, {value:-1,label:'赛区',children: []});
                    for (let i = 0 ; i < len; i++){
                        let temp={};
                        temp.value = this.competition.created_competition[index].list[i].id;
                        temp.label = this.competition.created_competition[index].list[i].value;
                        this.send_message_menu[1].children.push(temp);
                    }

                }
                else{
                    this.send_message_menu.splice(1,1);
                }
                */
                this.send_message_switch = 1;
            },
            SendMessageBack:function () {
                this.send_message_content = '';
                this.send_message_title = '';
                this.send_message_target = [];
                this.send_message_type = -1;
                this.send_message_contest = -1;
                this.send_message_switch = 0;
            },
            SendMessageSubmit:function () {
                let temp = {};
                temp.contestid = this.send_message_contest;
                temp.title = this.send_message_title;
                temp.content = this.send_message_content;
                temp.target = {};
                temp.target.id = this.send_message_target[this.send_message_target.length - 1];
                temp.target.type = Number(this.send_message_type);
                console.log(temp);
                let vm = this;
                axios.post('/api/admin/broadcast',temp)
                    .then(response=>{
                        if(response.data.msg ===''){
                            vm.$message({
                                message: '发布成功!',
                                type: 'success'
                            });
                        }
                        else{
                            vm.$message({
                                message: `发布失败! ${response.data.msg}`,
                                type: 'error'
                            });
                        }
                    })

            },

        }
    }
</script>

<style>
  .person-table-btn{
    text-decoration: none;
    color: initial;
  }

  .person-info-card-value{
    float: right;
    color: gray;
  }
  .profile-page{
    margin-top: 40px;
  }
  .send-message-input{
    margin-top: 30px;
    margin-bottom: 30px;
  }
  .send-message-input-title{
    margin-bottom: 20px;
  }
  .send-message-input-content{
    margin-top: 20px;

  }
  .send-message-btn{
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .send-message-select{
    margin-top: 20px;
    margin-bottom: 10px;
  }

</style>