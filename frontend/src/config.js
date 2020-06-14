import axios from 'axios'

export const URL =`${document.location.origin}/api`

export const RANGE = 3

export const backend = axios.create({
    baseURL: URL
})