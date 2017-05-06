<template>
  <div class="modal fade" id="delete-scheduler" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-sm" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h5 class="modal-title">删除任务</h5>
        </div>
        <div class="modal-body">
          确认删除吗?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-default pull-left" data-dismiss="modal" style="width:120px;">Close</button>
          <button type="button" class="btn btn-sm btn-danger" style="width:120px;" v-on:click="$parent.deleteItem">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>
