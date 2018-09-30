import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api';
axios.defaults.timeout = 10000;

const api = {
    job: '/scheduler',
    status: '/scheduler/status',
    pause: '/scheduler/{0}/pause',
    resume: '/scheduler/{0}/resume',
    execute: '/scheduler/{0}/execute'
};


const sche = {
    start: function() {
        return axios.post(api.status);
    },
    stop: function() {
        return axios.delete(api.status);
    },
    status: function() {
        return axios.get(api.status);
    },
    job: {
        select: function(params) {
            return axios.get(api.job,{
                params:params
            });
        },
        create: function(params) {
            return axios.post(api.job, params);
        },
        update: function(pk,params) {
            return axios.put(api.job + "/" + pk, params);
        },
        delete: function(pk) {
            return axios.delete(api.job + "/" + pk);
        },
        getitem: function(params) {
            return axios.get(api.job,{
                params:params
            });
        },
        deletelist: function(params) {
            return axios.put(api.job, params);
        },
        pause: function(pk) {
            return axios.post(api.pause.format(pk));
        },
        resume: function(pk) {
            return axios.post(api.resume.format(pk));
        },
        execute: function(pk) {
            return axios.post(api.execute.format(pk));
        },
    }
};
export default sche;
