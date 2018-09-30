<template>
  <div class="modal fade" id="create-job">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h5 class="modal-title" v-if="item.id">编辑任务</h5>
          <h5 class="modal-title" v-else>新建任务</h5>
        </div>
        <div class="modal-body" style="padding-bottom:0px;">
          <form class="form-horizontal" id="post-form">
            <div class="input-group">
              <span class="input-group-addon">定时类型</span>
              <select class="form-control" v-model="item.trigger">
                <option value="date">定时任务</option>
                <option value="interval">间隔时间任务</option>
              </select>
            </div>
            <div class="input-group">
              <span class="input-group-addon">任务列表</span>
              <select class="form-control" v-model="item.func">
                <option :value="job.name" v-for="job in jobs">{{ job.doc }}</option>
              </select>
            </div>
            <div class="input-group">
              <span class="input-group-addon">任务名</span>
              <input class="form-control" placeholder="name" v-model="item.name">
            </div>
            <div class="input-group">
              <span class="input-group-addon">函数参数</span>
              <input class="form-control" placeholder="kwargs" v-model="item.kwargs">
            </div>
            <template v-if="item.trigger=='date'">
              <div class="input-group">
                <span class="input-group-addon">运行时间</span>
                <input class="form-control" id="run_date" placeholder="run_date" v-model="item.run_date">
              </div>
            </template>
            <template v-else>
              <div class="input-group">
                <span class="input-group-addon">开始时间</span>
                <input class="form-control" id="start_date" placeholder="start_date" v-model="item.start_date">
              </div>
              <div class="input-group">
                <span class="input-group-addon">结束时间</span>
                <input class="form-control" id="end_date" placeholder="end_date" v-model="item.end_date">
              </div>
              <div class="input-group">
                <span class="input-group-addon">间隔时间</span>
                <input class="form-control" placeholder="seconds" v-model="item.seconds">
              </div>
            </template>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-default" data-dismiss="modal">Close</button>
          <button v-if="item.id" type="button" class="btn btn-sm btn-primary" v-on:click="update">保存</button>
          <button v-else type="button" class="btn btn-sm btn-primary" v-on:click="create">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="text/javascript">
 export default {
     data() {
         return {
             item: {
                 "trigger":"interval"
             },
             jobs:this.$parent.jobs,
         }
     },
     mounted() {
         this.daterangepicker("#run_date")
         this.daterangepicker("#start_date")
         this.daterangepicker("#end_date")
     },
     methods: {
         daterangepicker: function(id) {
             var options = {
                 parentEl: $('#create-job'),
                 autoUpdateInput: false,
                 singleDatePicker: true,
                 timePicker:true,
                 timePicker24Hour: true,
                 timePickerSeconds: true,
                 locale: {
                     format: 'YYYY-MM-DD hh:mm:ss'
                 }
             }
             $(id).daterangepicker(options);
             $(id).on('apply.daterangepicker', function(ev, picker) {
                 $(this).val(picker.startDate.format('YYYY-MM-DD hh:mm:ss'))
             });
             $(id).on('cancel.daterangepicker', function(ev, picker) {
                 $(this).val('');
             });
         },
         create: function() {
             if (this.item.trigger == 'interval') {
                 this.item.seconds = parseInt(this.item.seconds)
                 if (!this.item.start_date) {
                     delete this.item.start_date
                 }
                 if (!this.item.end_date) {
                     delete this.item.end_date
                 }
             }
             this.$parent.create(this.item)
         },
         update: function() {
             if (this.item.trigger == 'interval') {
                 this.item.seconds = parseInt(this.item.seconds)
                 if (!this.item.start_date) {
                     delete this.item.start_date
                 }
                 if (!this.item.end_date) {
                     delete this.item.end_date
                 }
             }
             this.$parent.updateItem(this.item)
         }
     }
 }
</script>
