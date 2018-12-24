<template>
  <div id="app">
    <el-container>
    <el-header height="100px" class="header">
      <div><NavigationBar :username="m_username"></NavigationBar></div>
    </el-header>

      <el-main>
        <el-row :gutter="0">
          <el-col :span="24" class="banner">报名比赛 </el-col>
        </el-row>

        <el-row :gutter="0" >
          <div class="enroll-info-spliter"> -----基本信息-----</div>
        </el-row>

        <el-row :gutter="0">
          <el-col :span="8" :offset="9">
            <UniversityPicker @new-university="UpdateUniversity"></UniversityPicker>
          </el-col>
        </el-row>

        <el-row :gutter="0">
          <el-col :span="12" :offset="6">
            <el-input type="text" v-model="phone_number" autocomplete="off">
              <span slot="prepend">联系电话</span>
            </el-input>
          </el-col>
        </el-row>


        <div v-if="enroll_table.comp_type === 0" class="group_enroll">
          <el-row :gutter="0">
            <el-col :span="12" :offset="6">
              <el-input type="text"  v-model="group_info.group_name" autocomplete="off">
                <span slot="prepend">队伍名称</span>
              </el-input>
            </el-col>
          </el-row>

          <el-row :gutter="0">
            <el-col :span="8" :offset="9">
              <GroupUser :competition_id="competition_id"
                         :group_min_number="enroll_table.group_min_number"
                         :group_max_number="enroll_table.group_max_number"
                         @new-group="UpdateGroup"></GroupUser>
            </el-col>
          </el-row>
        </div>

        <div v-else class="person_enroll">

          <!-- <el-row :gutter="0" class="enroll-info-spliter"> -->
          <!--  <el-col :span="12" :offset="6"> -----个人赛信息-----</el-col> -->
          <!-- </el-row> -->

        </div>


        <el-row v-if="extra_length!==0" :gutter="0" class="enroll-info-spliter">
          <el-col :span="12" :offset="6"> -----额外信息-----</el-col>
        </el-row>

        <div class="extra_info">
          <el-row :gutter="0" v-for="(item,index) in enroll_table.extra" :key="index">
            <el-col :span="12" :offset="6">
              <el-input type="text"  v-model="extra_info[index]" autocomplete="off">
                <span slot="prepend">{{item}}</span>
              </el-input>
            </el-col>
          </el-row>
        </div>

      <el-row :gutter="0" >
        <div class="enroll-btn" :span="12" :offset="6">
          <el-button type="text" @click="SubmitEnroll"> <span class="enroll-continue-btn">报名></span></el-button>
        </div>
      </el-row>

      </el-main>
    </el-container>
  </div>
</template>

<script>
    import NavigationBar from '../../components/NavigationBar'
    import GroupUser from '../../components/GroupUser'
    import UniversityPicker from '../../components/UniversityPicker'
    //import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        props:{
            enroll_table:{
                type: Object,
                default:function () {
                    return{
                        comp_type:0,
                        group_min_number:1,
                        group_max_number:1,
                        extra:[],
                    }
                }
            },
            competition_id:{
                default:-1,
            },
            m_username:{
                default:"",
                type:String
            }
        },
        data() {
            return {
                //essential infp
                region:{
                    province:'',
                    city:''
                },
                university:'',
                phone_number:'',
                //group info
                group_info:{
                    group_name:'',
                    group_member:[],
                    group_member_number:1,
                },
                //person info
                person_info:{
                },
                //extra info
                extra_info:[],
                extra_length:0,
            }
        },
        components: {
            NavigationBar,
            GroupUser,
            UniversityPicker,
        },
        mounted:function () {
            let vm = this;
            vm.extra_length = vm.enroll_table.extra.length;
            //for (let i = 0 ; i < vm.extra_length; i++){
            //    vm.$set(vm.extra_info,i,'');
            //}
            axios.post('/api/competition/neededinfo',{contestid:this.competition_id})
                .then(response=>{
                    vm.enroll_table = response.data;
                    vm.extra_length = vm.enroll_table.extra.length;
                    //console.log(vm.extra_length);
                    for (let i = 0 ; i < vm.extra_length; i++){
                        vm.$set(vm.extra_info,i,'');
                    }
                });

        },
        methods:{
            SubmitEnroll:function () {
                //Check Input
                //essential info
                if(this.university.length === 0){
                    this.$message({
                        message: "所在大学不能为空!",
                        type: 'error'
                    });
                    return;
                }

                if(this.phone_number.length === 0){
                    this.$message({
                        message: "联系电话不能为空!",
                        type: 'error'
                    });
                    return;
                }
                else{
                    if(! /\d{11}/.test(this.phone_number)){
                        this.$message({
                            message: "联系电话格式错误!",
                            type: 'error'
                        });
                        return;
                    }
                }



                //group info
                if(this.enroll_table.comp_type === 0) {
                    if (this.group_info.group_name.length === 0) {
                        this.$message({
                            message: "队伍名称不能为空!",
                            type: 'error'
                        });
                        return;
                    }
                    if (this.group_info.group_member_number < this.enroll_table.group_min_number - 1) {
                        this.$message({
                            message: `队伍至少需要${this.enroll_table.group_min_number - 1}名队员!`,
                            type: 'error'
                        });
                        return;
                    }
                }
                //person info
                else{
                    //console.log('check person info');
                }

                //extra info
                for (let i = 0 ; i < this.extra_length; i++){
                    if(this.extra_info[i].length === 0){
                        this.$message({
                            message: `${this.enroll_table.extra[i]} 不能为空!`,
                            type: 'error'
                        });
                        return;
                    }
                }

                //if all check has passed
                let enroll_info = {};
                //enroll_info.comp_type = this.enroll_table.comp_type;
                if(this.enroll_table.comp_type === 0){
                    enroll_info.groupuser = this.group_info.group_member;
                    enroll_info.groupname = this.group_info.group_name;
                }
                else{
                    enroll_info.groupuser = [];
                    enroll_info.groupname = '';
                }
                //extra_info
                enroll_info.custom_field = this.enroll_table.extra;
                enroll_info.custom_value = this.extra_info;
                enroll_info.contestid = this.competition_id
                enroll_info.username = this.m_username;
                enroll_info.university = this.university;
                enroll_info.phone_number = this.phone_number;
                console.log(enroll_info);
                axios.post('/api/competition/enroll',enroll_info)
                    .then(response=>{
                        let vm = this;
                        if (response.data.msg==='') {
                            //成功
                            vm.$message({
                                message: '报名成功!',
                                type: 'success'
                            });
                            window.location.href = '/';
                        }
                        else{
                            //失败
                            vm.$message({
                                message: response.data.msg,
                                type: 'error'
                            });
                        }
                    });
            },
            UpdateRegion:function (value) {
                this.region.province = value.province.value;
                this.region.city = value.city.value;
            },
            UpdateGroup:function(data){
                this.group_info.group_member = data.value;
                this.group_info.group_member_number = data.number;
            },
            UpdateUniversity:function (data) {
                this.university = data;
            },
        }
    }
</script>

<style>
  .banner{
    font-size:30px;
    background: #F0F8FF;
    text-align: center;
    font-family: "PingFang SC";
    padding: 40px 0px 40px 0px;
  }

  .el-row{
    margin-top: 20px;
  }

  .enroll-continue-btn{
      font-size: 16px;
      text-align: center;
  }
  .enroll-info-spliter{
    font-size: 20px;
    font-family: "PingFang SC";
    margin-top: 30px;
    margin-bottom: 30px;
    text-align: center;
  }
  .enroll-btn{
    text-align: center;
  }

</style>