export default function SuggestionCard({suggestion}){

 return(

  <div className="bg-gray-900 p-4 mb-3 rounded">

    <p>{suggestion.issue}</p>

    <p>{suggestion.fix}</p>

  </div>

 )
}
