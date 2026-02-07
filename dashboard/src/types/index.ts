export interface Suggestion{
  issue:string
  fix:string
}

export interface Result{
  performance_score:number
  lcp:number
  cls:number
  tbt:number
  ai_explanation:string[]
  suggestions:Suggestion[]
}
