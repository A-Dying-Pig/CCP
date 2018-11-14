<template>
    <div class = "region-picker">
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
        components: { VDistpicker },
        methods: {
            onSelected:function(data) {
                this.province = data.province.value;
            },
          }
    }
</script>

<style>
</style>