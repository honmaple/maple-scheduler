<template>
  <div class="text-left" style="margin-bottom:7px;">
    <button type="button" class="btn btn-sm btn-primary opeara" v-on:click="start">启动</button>
    <button type="button" class="btn btn-sm btn-warning opeara" v-on:click="stop">关闭</button>
    <button type="button" class="btn btn-sm btn-success" >状态: {{ status }}···</button>
  </div>
</template>

<script type="text/javascript">
 import {status} from 'service'

 export default {
     data() {
         return {
             status:'停止'
         }
     },
     mounted() {
         status.get().then((response) => {
             if (response.data.data.running) {
                 this.status = '正在运行'
             }else {
                 this.status = '停止'
             }
         }).catch(function(response) {
             console.log(response)
         })
     },
     methods: {
         start: function() {
             status.post({}).then((response) => {
                 this.status = '正在运行'
             }).catch(function(response) {
                 console.log(response)
             })
         },
         stop: function() {
             status.delete({}).then((response) => {
                 this.status = '停止'
             }).catch(function(response) {
                 console.log(response)
             })
         },
     }
 }
</script>
