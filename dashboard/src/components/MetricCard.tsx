export default function MetricCard({title,value}){

 return(
  <div className="bg-gray-900 p-4 rounded">
    <p>{title}</p>
    <h2>{value}</h2>
  </div>
 )
}
