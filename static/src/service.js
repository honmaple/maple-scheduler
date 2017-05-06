import axios from 'axios'
import api from 'api'

// axios.interceptors.request.use(function (config) {
//   // config.params.cloud_token = 'MQ.C6GeUA.4l_y_wIqC70ER2hzMbUWL4Kkf4c'
//   var token = sessionStorage.getItem('token');
//   config.headers['Cloud-Token'] = token;
//   return config;
// }, function (error) {
//   return Promise.reject(error);
// });

export var scheduler = {
  getlist: function(params) {
    return axios.get(api.scheduler,{
      params:params
    });
  },
  get: function(pk) {
    return axios.get(api.scheduler + '/' + pk);
  },
  post: function(data) {
    return axios.post(api.scheduler,data);
  },
  put: function(pk,data) {
    return axios.put(api.scheduler + '/' + pk,data);
  },
  delete: function(pk) {
    return axios.delete(api.scheduler + '/' + pk);
  },
  pause: function(pk) {
    return axios.post(api.pause.format(pk));
  },
  resume: function(pk) {
    return axios.post(api.resume.format(pk));
  },
  execute: function(pk) {
    return axios.post(api.execute.format(pk));
  }
}

export var status = {
  get: function() {
    return axios.get(api.status);
  },
  post: function(data) {
    return axios.post(api.status,data);
  },
  delete: function(data) {
    return axios.delete(api.status,data);
  },
}

export function jobs() {
  return axios.get(api.jobs);
}
