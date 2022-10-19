const URL = "http://127.0.0.1:8000/demo/"

//USED TO GET INFO ABOUT QUEE FROM SERVER
async function getAllInfos(){
    const response = await fetch(URL+'Services/');
    const services = await response.json();
    if(response.ok){
        return services.map((c) => ({tag:c[0], name:c[1], last:c[2], actual: c[3]}))
    } else {
        throw services;
    }
}
async function postQueue(service) {
  let response = await fetch(URL+'Ticket', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 'service_name': service}),
  });
  if (response.ok) {
    const queue = await response.json();
    return queue;
  } else {
    const errDetail = await response.json();
    throw errDetail.message;
  }
}

  async function login(credentials) {
    let response = await fetch(URL+'sessions', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    if (response.ok) {
      const user = await response.json();
      return user;
    } else {
      const errDetail = await response.json();
      throw errDetail.message;
    }
  }
  
  async function logout() {
    await fetch(URL+'sessions/current', { method: 'DELETE', credentials: 'include' });
  }
  
  async function getUserInfo() {
    const response = await fetch(URL+'sessions/current', {credentials: 'include'});
    const userInfo = await response.json();
    if (response.ok) {
      return userInfo;
    } else {
      throw userInfo;  // an object with the error coming from the server
    }
  }

  async function nextClient(counter){
    const response = await fetch(URL+'NextClient', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'counter_id': counter}),
    });
    const next = await response.json();
    if (response.ok){
      return next;
    }else
    {
      throw next;
    }
  }

  async function update(){
    const response = await fetch(URL+'Statistics/',{method: 'GET', credential: 'include'});
    const up=await response.json();
    if (response.ok){
      return up;
    }else{
      throw up;
    }
  }

const API = {getAllInfos,login,logout, getUserInfo,postQueue,nextClient,update};
export default API;
