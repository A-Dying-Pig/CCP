<template>
    <div class="MdEdit">{{ title }}<Simditor v-bind:content="conten" v-on:change="$emit('input', $event)"></Simditor></div>
</template>

<script>
    import Simditor from 'vue-simditor'
    export default {
        components: {
            Simditor
        },
        props:['title','value'],
        data() {
            return {
                conten:this.value,
            }
        },
    }
</script>