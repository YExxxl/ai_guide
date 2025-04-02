import axios from "axios"
var instance = axios.create({
    timeout: 20000,
})

export let $get = async (url, params)=>{
    let {data} = await instance.get(url, {params})
    return data
}

export let $post = async (url, params)=>{
    let {data} = await instance.post(url, params)
    return data
}
