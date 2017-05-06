<template>
  <div class="scheduler-list">
    <div class="container-fluid">
      <ol class="breadcrumb text-left">
        <li><a href="#">定时任务管理</a></li>
        <li class="active">任务列表</li>
      </ol>
      <div>
        <div class="pull-right">
          <form class="form-inline">
            <div class="form-group">
              <input type="text" class="form-control input-sm" id="start" placeholder="定时任务ID" style="border-radius:3px 0 0 3px">
              <!-- <button type="button" class="btn btn-sm btn-primary pull-right" style="width:100px;border-radius:0 3px 3px 0;">搜索</button> -->
            </div>
          </form>
        </div>
        <status-template></status-template>
      </div>
      <div>
        <div class="pull-right">
          <select class="form-control input-sm pull-right" style="padding:2px;">
            <option>全部</option>
            <option>定时任务</option>
            <option>间隔时间任务</option>
          </select>
        </div>
        <div class="text-left">
          <template v-if="ischecked">
            <button type="button" class="btn btn-sm btn-warning opeara" v-on:click="selectAll">取消全选</button>
          </template>
          <template v-else>
            <button type="button" class="btn btn-sm btn-primary opeara" v-on:click="selectAll">全选</button>
          </template>
          <button type="button" class="btn btn-sm btn-danger opeara">删除选中</button>
          <button type="button" class="btn btn-sm btn-success opeara"  @click="_postItem">新建任务</button>
        </div>
      </div>
      <hr/>
      <table class="table table-hover table-striped table-bordered">
        <thead>
          <tr>
            <th v-for="th in table.th">{{ th }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td style="width:45px;"><input type="checkbox" :value="item.id" v-model="checked"></td>
            <td>{{ item.name }}</td>
            <td>{{ item.next_run_time }}</td>
            <td>{{ item.pending }}</td>
            <td style="width:240px;">
              <div class="btn-group btn-group-justified" role="group" style="margin-bottom:7px;">
                <a class="btn btn-sm btn-warning opeara-item" v-on:click="getItem(item.id)">查看</a>
                <a class="btn btn-sm btn-success opeara-item" v-on:click="_updateItem(item.id)">修改</a>
                <a class="btn btn-sm btn-danger opeara-item" v-on:click="_deleteItem(item.id)">删除</a>
              </div>
              <div class="btn-group btn-group-justified" role="group">
                <a class="btn btn-sm btn-warning opeara-item" @click="pauseItem(item.id)">暂停</a>
                <a class="btn btn-sm btn-success opeara-item" @click="resumeItem(item.id)">恢复</a>
                <a class="btn btn-sm btn-danger opeara-item" @click="executeItem(item.id)">执行</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <span class="text-center notfound" v-if="items.length == 0">
        暂无定时任务
      </span>
    </div>
    <post-template ref="post"></post-template>
    <get-template ref="get"></get-template>
    <delete-template ref="delete"></delete-template>
  </div>
</template>

<script>
 import {lazyload} from 'globals'
 import {scheduler} from 'service'

 export default {
     components: {
         'post-template':lazyload('post'),
         'delete-template':lazyload('delete'),
         'get-template':lazyload('item'),
         'status-template':lazyload('status'),
     },
     data() {
         return {
             table: {
                 'th': ['选择', '任务名称', '下次运行时间', '运行状态', '操作']
             },
             items: [],
             pageinfo: {},
             checked:[],
             ischecked:false,
             operaId:null
         }
     },
     created() {
         this.getItemList()
     },
     methods: {
         getItemList: function() {
             scheduler.getlist({}).then((response) => {
                 this.items = response.data.data
                 this.pageinfo = response.data.pageinfo
             }).catch(function(response) {
                 console.log(response)
             })
         },
         getItem: function(pk) {
             scheduler.get(pk).then((response) => {
                 this.$refs.get.item = response.data.data
             }).catch(function(response) {
                 console.log(response)
             })
             $('#get-scheduler').modal('toggle')
         },
         _postItem: function() {
             this.$refs.post.getJobList()
             $('#post-scheduler').modal('toggle')
         },
         postItem: function(form) {
             scheduler.post(form).then((response) => {
                 this.items.push(response.data.data)
             }).catch(function(response) {
                 console.log(response)
             })
             $('#post-scheduler').modal('hide')
         },
         _updateItem: function(pk) {
             this.operaId = pk
             this.$refs.post.getJobList()
             scheduler.get(pk).then((response) => {
                 var item = response.data.data
                 var form = this.$refs.post.form
                 form.name = item.name
                 /* form.func = item.func*/
             }).catch(function(response) {
                 console.log(response)
             })
             $('#post-scheduler').modal('toggle')
         },
         updateItem: function(schedulerId) {
             this.schedulerId = schedulerId
             $('#update-scheduler').modal('toggle')
         },
         _deleteItem: function(pk) {
             this.operaId = pk
             $('#delete-scheduler').modal('toggle')
         },
         deleteItem: function() {
             scheduler.delete(this.operaId).then((response) => {
                 this.getItemList()
             }).catch(function(response) {
                 console.log(response)
             })
             $('#delete-scheduler').modal('hide')
         },
         pauseItem: function(pk) {
             scheduler.pause(pk).then((response) => {
                 console.log(response)
             }).catch(function(response) {
                 console.log(response)
             })
         },
         resumeItem: function(pk) {
             scheduler.resume(pk).then((response) => {
                 console.log(response)
             }).catch(function(response) {
                 console.log(response)
             })
         },
         executeItem: function(pk) {
             scheduler.execute(pk).then((response) => {
                 console.log(response)
             }).catch(function(response) {
                 console.log(response)
             })
         },
         selectAll: function(event) {
             this.ischecked = !this.ischecked
         },
         deleteSelected: function(event) {
             alert('s')
         },
     },
     watch: {
         checked: function () {
             if (this.checked.length == this.items.length) {
                 this.ischecked = true
             }
         },
         ischecked: function () {
             if (this.ischecked) {
                 this.checked = this.items.map(function(item) {
                     return item.id
                 })
             }else {
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
