<template>
<div class="competition-profile-unit"
                 :style="{width:w +'px'}"
                 style="white-space:normal;word-break:break-all;text-overflow: ellipsis"
            >
                <img
                    v-bind:src=img_url
                    :style="{width:w+'px',height:w+'px'}"
                >
                <br>
                <span><center>{{title}}</center></span>
                <p>{{intro}}</p>
            </div>
</template>

<script>
export default{
props:{
        w:{
            type:Number,
            default:200,
        },
        h:{
            type:Number,
            default:400,
        },
        img_url: {
            type: String,
            default: ''
        },
        title:{
            type:String,
            default:''
        },
        intro:{
            type:String,
            default:''
        },
        comp_url:{
            type:String,
            default:''
        }
    },

}
</script>

<style>

</style>