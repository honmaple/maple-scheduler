<template>
  <div class="container-fluid">
    <div>
      <div class="pull-right">
        <select class="form-control input-sm pull-right" style="padding:2px;" v-model="trigger">
          <option value="all">全部</option>
          <option value="date">定时任务</option>
          <option value="interval">间隔时间任务</option>
        </select>
      </div>
      <div class="text-left">
        <button type="button" class="btn btn-sm btn-success" title="关闭" v-if="running" v-on:click="stop">状态: 正在运行···</button>
        <button type="button" class="btn btn-sm btn-warning" title="启动" v-else v-on:click="start">状态: 停止···</button>
        <button type="button" class="btn btn-sm btn-danger" v-on:click="deleteSelected" v-if="checked.length > 0">删除选中</button>
        <button type="button" class="btn btn-sm btn-success" data-toggle="modal" data-target="#create-job">新建任务</button>
      </div>
    </div>
    <hr/>
    <table class="table table-hover table-striped table-bordered">
      <thead>
        <tr>
          <th><input type="checkbox" v-model="selectAll"></th>
          <th v-for="th in table.th">{{ th }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items">
          <td style="width:45px;"><input type="checkbox" :value="item.id" v-model="checked"></td>
          <td>{{ item.name }}</td>
          <td>{{ item.next_run_time }}</td>
          <td>{{ item.pending }}</td>
          <td style="width:240px;">
            <div class="btn-group btn-group-justified" role="group" style="margin-bottom:7px;">
              <a class="btn btn-sm btn-success opeara-item"
                 @click="edit(index, item.id)">修改</a>
              <a class="btn btn-sm btn-danger opeara-item"
                 @click="_remove(index, item.id)">删除</a>
            </div>
            <div class="btn-group btn-group-justified" role="group">
              <a class="btn btn-sm btn-success opeara-item"
                 @click="execute(item)">执行</a>
              <a class="btn btn-sm btn-danger opeara-item"
                 @click="pause(item)"
                 v-if="item.next_run_time">暂停</a>
              <a class="btn btn-sm btn-warning opeara-item"
                 @click="resume(item)"
                 v-else>恢复</a>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <span class="text-center notfound" v-if="items.length == 0">
      暂无定时任务
    </span>
    <create-template ref="'create'"></create-template>
    <delete-template ref="'delete'"></delete-template>
  </div>
</template>

<script>
 import {lazyload} from 'globals'
 import sche from 'api'

 export default {
     components: {
         'create-template':lazyload('create'),
         'delete-template':lazyload('delete'),
     },
     data() {
         return {
             table: {
                 'th': ['任务名称', '下次运行时间', '运行状态', '操作']
             },
             items: [],
             pageinfo: {},
             checked:[],
             ischecked:false,
             operaId:null,
             trigger:'all',
             running: false,
             jobs:[],
             selectAll:[]
         }
     },
     created() {
         sche.status().then((response) => {
             this.running = response.data.data.running
             this.jobs = response.data.data.funcs
             this.$refs.create.jobs = this.jobs
         }).catch(error => {
             console.log(error)
         })
         this.select()
     },
     methods: {
         select: function() {
             var params = {
                 'trigger':this.trigger
             }
             sche.job.select(params).then((response) => {
                 this.items = response.data.data
             }).catch(error => {
                 console.log(error)
             })
         },
         create: function(item) {
             sche.job.create(item).then(response => {
                 this.items.push(response.data.data)
             }).catch(error => {
                 console.log(error)
             })
             $('#create-job').modal('hide')
         },
         edit: function(index,pk) {
             this.$refs.create.item = this.items[index];
             $('#create-job').modal('toggle')
         },
         update: function(item) {
             sche.job.update(this.item.id, item).then(response => {
                 this.select()
             }).catch(error => {
                 console.log(error)
             })
             $('#create-job').modal('toggle')
         },
         _remove: function(index, pk) {
             this.operaId = pk
             $('#delete-job').modal('toggle')
         },
         remove: function() {
             sche.job.delete(this.operaId).then(response => {
                 this.select()
             }).catch(error => {
                 console.log(error)
             })
             $('#delete-job').modal('hide')
         },
         pause: function(item) {
             sche.job.pause(item.id).then(response => {
                 item.next_run_time = null
             }).catch(error => {
                 console.log(error)
             })
         },
         resume: function(item) {
             sche.job.resume(item.id).then(response => {
                 item.next_run_time = response.data.data.next_run_time
             }).catch(error => {
                 console.log(error)
             })
         },
         execute: function(item) {
             sche.job.execute(item.id).then(response => {
                 console.log(response)
             }).catch(error => {
                 console.log(error)
             })
         },
         deleteSelected: function() {
             sche.job.deletelist({jobs:this.checked}).then(response => {
                 this.items = this.items.filter(item=> {
                     return response.data.data.indexOf(item.id) == -1;
                 })
             }).catch(error => {
                 console.log(error)
             })
         },
         start: function() {
             sche.start().then((response) => {
                 this.running = response.data.data.running
             }).catch(error => {
                 console.log(error)
             })
             this.select()
         },
         stop: function() {
             sche.stop().then((response) => {
                 this.running = response.data.data.running
             }).catch(error => {
                 console.log(error)
             })
         },
     },
     watch: {
         trigger: function () {
             this.select()
         },
         selectAll: function() {
             if (this.selectAll.length > 0) {
                 this.checked = this.items.map(item => {
                     return item.id
                 })
             }else{
                 this.checked = []
             }
         }
     }
 }
</script>

<style>
 .opeara {
     width: 85px;
 }

 .opeara-item {
     width: 56px;
 }
 /* .scheduler-list {
    background-color: #f5f5f5;
    border-radius: 4px;
    } */

 .breadcrumb {
     background-color: #fff;
 }
 .notfound {
     display:block;
     color:#999;
     border:1px solid #eee;
     padding:15px;
     margin-top:-20px;
     border-top:none;
 }
</style>
