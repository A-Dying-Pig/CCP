<template>
  <div id="app">
    <el-container>
    <el-header height="100px" class="header">
      <div><NavigationBar :username="musername"></NavigationBar></div>
    </el-header>

      <el-main>
        <el-row :gutter="20">
          <el-col :span="24" ><IndexSlider :sliders="slider_info"></IndexSlider> </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="23" :offset="1">
            <div class="hot-competitions-spliter">
              热门比赛
              <hr>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="5" :offset="1" v-for="(item,index) in hot_info" :key="index">
            <CompetitionProfile :competition_profile="item"></CompetitionProfile>
          </el-col>
        </el-row>

    </el-main>
    </el-container>

    <el-container>
      <el-footer>
        <CCPFooter></CCPFooter>
      </el-footer>
    </el-container>

  </div>
</template>

<script>

    import NavigationBar from '../../components/NavigationBar'
    import IndexSlider from '../../components/IndexSlider'
    import CompetitionProfile from '../../components/CompetitionProfile'
    import CCPFooter from '../../components/CCPFooter'
    import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        props:{
            musername:{
                default:'',
                type:String
            }
        },
        name: 'app',
        data() {
            return {
                slider_info:[{url:'/index',img_url:require('../../assets/img/comp1.jpg')},
                    {url:'/index',img_url:require('../../assets/img/comp2.jpg')}],//{url: img_url}
                hot_info:[{url:'/index',img:require('../../assets/img/logo.png'),title:'比赛示例1',intro:'比赛介绍1'},
                    {url:'/index',img:require('../../assets/img/logo.png'),title:'比赛示例2',intro:'比赛介绍2'},
                    {url:'/index',img:require('../../assets/img/logo.png'),title:'比赛示例3',intro:'比赛介绍3'},
                    {url:'/index',img:require('../../assets/img/logo.png'),title:'比赛示例4',intro:'比赛介绍4'}],  //{url: img_url: title: intro:}
            }
        },
        components: {
            NavigationBar,
            IndexSlider,
            CompetitionProfile,
            CCPFooter
        },
        mounted:function () {
            let vm = this;
            axios.get('/api/competition/slider')
                .then(response=>{
                    vm.slider_info = response.data;
                });
            axios.get('/api/competition/hot')
                .then(response=>{
                    vm.hot_info = response.data;
                })
        }
    }
</script>

<style>
  .hot-competitions-spliter{
    font-family: PingFang SC;
    font-size: 20px;
    color: darkblue;
    margin-top: 10px;
    margin-bottom: 20px;
  }

</style>