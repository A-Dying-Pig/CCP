<template>
    <div class="MdEdit"><slot></slot><Simditor v-bind:content="conten" v-on:change="$emit('input', $event)"></Simditor></div>
</template>

<script>
    import Simditor from 'vue-simditor'
    export default {
        components: {
            Simditor
        },
        props:['value'],
        data() {
            return {
                conten:this.value,
            }
        },
    }
</script>