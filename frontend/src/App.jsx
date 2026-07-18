import { useState } from 'react'

function App(){
  const [input,setInput] = useState('')
  const [result,setResult] = useState(null)
  const [loading,setLoading] = useState(false)

  const handleAnalyze = async () =>{
    setLoading(true)
    setResult(null)
    try{
      const response = await fetch('http://127.0.0.1:8000/api/analyze',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body:JSON.stringify({content: input})
      })
      const data = await response.json()
      setResult(data)
    }
    catch(error){
      console.error("Error connecting to the lens:",error)
    }
    finally{
      setLoading(false)
    }

  }
return (
  <div>
    <h1>TruthLens: The Morning Edition</h1>
    
    <textarea 
      value={input}
      onChange={(e) => setInput(e.target.value)}
      style={{ display: 'block', marginBottom: '1rem', width: '100%', height: '150px' }}
      placeholder="Paste the ink here..."
    />
    
    <button onClick={handleAnalyze} disabled={loading}>
      {loading ? 'Eyes are opening...' : 'Dissect the Ink'}
    </button>

    {result && (
      <div style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem' }}>
        <h3>The Occular Dossier:</h3>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </div>
    )}
  </div>
)
}
