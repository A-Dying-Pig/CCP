<template>
    <div class = "region-picker">
        <span class='region-picker-label'>所在地区</span>
        <v-distpicker  hide-area @selected="onSelected"></v-distpicker>
    </div>
</template>


<script>
    import VDistpicker from 'v-distpicker'

    export default {
        name:"RegionPicker",
        data:function(){
            return{
            }
        },
        components: { VDistpicker },
        methods: {
            onSelected:function(data) {
                this.$emit('new-region',data);
            },
          }
    }
</script>

<style>
.distpicker-address-wrapper{
    display:inline
}

.region-picker-label{
    margin-right:20px;
    font-size:16px;
}
</style>