<template>
    <div class="modal fade" id="update-scheduler" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-sm" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h5 class="modal-title">修改任务</h5>
                </div>
                <div class="modal-body" style="padding-bottom:0px;">
                    {{ schedulerId }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-sm btn-default pull-left" data-dismiss="modal" style="width:120px;">Close</button>
                    <button type="button" class="btn btn-sm btn-primary" style="width:120px;">确定</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {
        props: ['schedulerId'],
    }
</script>
