export type User={id:number;name:string;username:string;email:string}
export type Course={id:number;name:string;code?:string;description?:string}
export type Task={id:number;title:string;description?:string;due_date:string;course_id:number;is_completed:boolean}
export type Exam={id:number;title:string;exam_date:string;location?:string;notes?:string;course_id:number}
export type Dashboard={upcoming_tasks:Task[];upcoming_exams:Exam[];completed_tasks:Task[];total_courses:number}
const key='studyPlannerToken'
export const getToken=()=>localStorage.getItem(key)
export const setToken=(v:string)=>localStorage.setItem(key,v)
export const clearToken=()=>localStorage.removeItem(key)
export async function api<T>(path:string,options:RequestInit={}):Promise<T>{const headers=new Headers(options.headers);const token=getToken();if(token)headers.set('Authorization',`Bearer ${token}`);if(options.body&&!(options.body instanceof URLSearchParams))headers.set('Content-Type','application/json');const response=await fetch(path,{...options,headers});if(!response.ok){let message='İşlem gerçekleştirilemedi.';try{const data=await response.json();if(typeof data.detail==='string')message=data.detail}catch{}throw new Error(message)}return response.status===204?undefined as T:response.json()}
