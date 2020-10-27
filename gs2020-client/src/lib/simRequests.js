import axios from 'axios';

const serverAddress = 'http://localhost:5000';

export default {
  connectSim: async () =>  {
    const result = await axios.get(`${serverAddress}/connect`);
    return result;
  },
  getDataset: async (dataSet) => {
    const result = await axios.get(`${serverAddress}/dataset/${dataSet}`);
    return result.data;
  },
  getSimVar: async (simVar) => {
    const result = await axios.get(`${serverAddresss}/dataset/${dataSet}`);
    return result.data;
  },
  setSimVar: async (simVar, value, index = null) => {
    const requestObject = {
      'value_to_use': value
    };
    index !== null && (requestObject.index = index);
    const response = await axios.post(`${serverAddress}/datapoint/${simVar}/set`, requestObject);
    return response;
  },
  sendEvent: async (event, value) => {
    const result = await axios.post(`${serverAddress}/event/${event}/trigger`, { value_to_use: value });
    return result;
  },
};
