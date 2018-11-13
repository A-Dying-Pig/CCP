<template>
    <div class = "region-picker">
        <label class="region-picker-label">{{label}} </label>
        <v-distpicker  only-province @selected="onSelected"></v-distpicker>
    </div>
</template>


<script>
    import VDistpicker from 'v-distpicker'

    export default {
        name:"RegionPicker",
        data:function(){
            return{
                province:null,
            }
        },
        props:{
            label:{
                default:"工作省份:",
                type:String
            }
        },
        components: { VDistpicker },
        methods: {
            onSelected:function(data) {
                this.province = data.province.value;
            },
          }
    }
</script>

<style>
    .region-picker{
        width:600px;
    }

    .region-picker-label{
        font-size:16px;
    }
</style>