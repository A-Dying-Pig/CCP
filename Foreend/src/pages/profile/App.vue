<template>
  <div id="app">
    <el-container>
      <el-header height="100px" class="header">
        <div><NavigationBar :username="username"></NavigationBar></div>
      </el-header>
    </el-container>

    <el-container>
      <el-aside width="250px">
        <PersonPhoto :img_url="img_url"></PersonPhoto>

        <div class="person-center-aside-menu">
        <el-menu default-active="1" @select="UpdateMenu">
          <el-menu-item index="1">
            <i class="el-icon-document"></i>
            <span slot="title">相关比赛</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-setting"></i>
            <span slot="title">个人信息设置</span>
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
                  </template>
                </el-table-column>
              </el-table>
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
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        name: 'app',
        props:{
            username:{
                default:'',
                type:String
            }
        },
        data() {
            return{
                img_url:require('../../assets/img/logo.png'),
                activeName: '1',
                which_menu:'1',    //1 competitions; 2 settings
                competition:{
                    participated_competition:[{url:'/comp1',title:'我参加的比赛1'},{url:'/comp2',title:'我参加的比赛2'}],
                    created_competition:[{url:'/comp3',title:'我创建的比赛3'},{url:'/comp4',title:'我创建的比赛4'}],
                    rated_competition:[{url:'/comp5',title:'我参评的比赛5'},{url:'/comp6',title:'我参评的比赛6'}],
                },
                person:{
                    university:'清华大学',
                    region:{
                        province:'陕西省',
                        city:'西安市'
                    }
                },
                new_person:{
                    university:'清华大学',
                    region:{
                        province:'陕西省',
                        city:'西安市'
                    }
                },
                info_saved:true,
            }
        },
        components: {
            NavigationBar,
            PersonPhoto,
            RegionPicker,
            UniversityPicker
        },
        mounted:function () {
            axios.post('/api/PersonCenter')
                .then(response=>{
                  this.img_url = response.data.img_url;
                  this.competition = response.data.competition;
                  this.person = response.data.person;
                  this.new_person = this.person
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
                axios.post('/api/SetPerson',this.new_person);
                this.person = this.new_person;
                this.info_saved = true;
            },
            UpdateRegion:function (value) {
                this.new_person.region.province = value.province.value;
                this.new_person.region.city = value.city.value;
            },
            UpdateUniversity:function (data) {
                this.new_person.university = data;
            }
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
</style>