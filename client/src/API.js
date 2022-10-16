const URL = "http://localhost:3001/"

//USED TO GET INFO ABOUT QUEE FROM SERVER
async function getAllInfos(){
    const response = await fetch(URL);
    const services = await response.json();
    if(response.ok){
        return services.map((c) => ({id:c.id, info1:c.info1, info2:c.info2, info3:c.info1info3}))
    } else {
        throw services;
    }
}
async function postQueue(n) {
  let response = await fetch(URL, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(n),
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

const API = {getAllInfos,login,logout, getUserInfo,postQueue};
export default API;
