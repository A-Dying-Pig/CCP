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
    //import axios from 'axios'

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
                slider_info:[],//{url: img_url}
                hot_info:[],  //{url: img_url: title: intro:}
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
                    vm.slider_info = response.data.array;
                });
            axios.get('/api/competition/hot')
                .then(response=>{
                    vm.hot_info = response.data.array;
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