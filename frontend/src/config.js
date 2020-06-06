import axios from 'axios'

export const URL ='http://localhost:5000'

export const RANGE = 3

export const backend = axios.create({
    baseURL: URL
})