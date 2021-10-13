import axios from 'axios';
import qs from 'qs';
import { makeUseAxios } from 'axios-hooks';

const instance = axios.create({
  baseURL: '',
  paramsSerializer: (params) => {
    return qs.stringify(params, {
      skipNulls: true,
    });
  },
});

export const useAxios = makeUseAxios({
  axios: instance,
});

export default instance;
