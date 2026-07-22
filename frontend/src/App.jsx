import { useState } from 'react'

function App() {
  const [mode, setMode] = useState('text') // 'text' | 'url' | 'pdf'
  const [input, setInput] = useState('')
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    setLoading(true)
    setResult(null)

    try {
      let response;

      if (mode === 'pdf') {
        if (!file) {
          alert("Please select a PDF document first.")
          setLoading(false)
          return
        }
        const formData = new FormData()
        formData.append('file', file)
        
        response = await fetch('http://127.0.0.1:8000/api/analyze-pdf', {
          method: 'POST',
          body: formData,
        })
      } else {
        if (!input.trim()) {
          alert("Please enter text or a URL to analyze.")
          setLoading(false)
          return
        }
        const payload = mode === 'url' ? { url: input } : { content: input }

        response = await fetch('http://127.0.0.1:8000/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
      }

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("Error connecting to the lens:", error)
      alert("Failed to reach the TruthLens engine. Ensure FastAPI is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      {/* Header Newspaper Banner */}
      <header style={styles.header}>
        <div style={styles.topBar}>SPECIAL EDITION • VOL. I • ZERO-COST AI DOSSIER</div>
        <h1 style={styles.title}>TRUTHLENS</h1>
        <div style={styles.subTitle}>"The Ocular Investigation of Online Credibility"</div>
        <div style={styles.dividerDouble}></div>
      </header>

      {/* Input Mode Selector */}
      <div style={styles.tabContainer}>
        <button 
          onClick={() => { setMode('text'); setInput(''); }} 
          style={mode === 'text' ? styles.activeTab : styles.tab}
        >
          Raw Article Ink
        </button>
        <button 
          onClick={() => { setMode('url'); setInput(''); }} 
          style={mode === 'url' ? styles.activeTab : styles.tab}
        >
          Scrape News URL
        </button>
        <button 
          onClick={() => { setMode('pdf'); setFile(null); }} 
          style={mode === 'pdf' ? styles.activeTab : styles.tab}
        >
          Upload PDF File
        </button>
      </div>

      {/* Input Area */}
      <div style={styles.inputSection}>
        {mode === 'text' && (
          <textarea 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={styles.textarea}
            placeholder="Paste raw article text here..."
          />
        )}

        {mode === 'url' && (
          <input 
            type="url"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={styles.textInput}
            placeholder="Paste news URL (e.g., https://apnews.com/article/...)"
          />
        )}

        {mode === 'pdf' && (
          <div style={styles.fileDropZone}>
            <input 
              type="file" 
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              style={styles.fileInput}
            />
            {file && <p style={styles.fileName}>Selected Document: <strong>{file.name}</strong></p>}
          </div>
        )}

        <button 
          onClick={handleAnalyze} 
          disabled={loading}
          style={loading ? styles.buttonDisabled : styles.button}
        >
          {loading ? 'SCANS IN PROGRESS...' : 'DISSECT THE INK'}
        </button>
      </div>

      {/* Results Section */}
      {result && result.status === 'success' && (
        <main style={styles.dossier}>
          <div style={styles.dossierHeader}>
            <span style={styles.dossierStamp}>VERIFIED DOSSIER</span>
            <h2 style={styles.dossierTitle}>THE OCULAR REPORT</h2>
          </div>

          {/* Metadata Bar */}
          {result.data.metadata && (
            <div style={styles.metaBox}>
              <div><strong>TITLE:</strong> {result.data.metadata.title}</div>
              <div><strong>AUTHOR:</strong> {result.data.metadata.author}</div>
              <div><strong>DATE:</strong> {result.data.metadata.publication_date}</div>
            </div>
          )}

          {/* Summary & Missing Context Grid */}
          <div style={styles.grid}>
            <div style={styles.card}>
              <h3 style={styles.cardHeader}>NEUTRALIZED SUMMARY</h3>
              <p style={styles.cardText}>{result.data.objective_summary}</p>
            </div>

            <div style={styles.cardHighlight}>
              <h3 style={styles.cardHeaderAlert}>RAG SEARCH VERDICT</h3>
              <p style={styles.cardText}>{result.data.missing_context}</p>
            </div>
          </div>

          {/* Extracted Claims */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>EXTRACTED CLAIMS UNDER INVESTIGATION</h3>
            <ul style={styles.claimsList}>
              {result.data.extracted_claims.map((claim, idx) => (
                <li key={idx} style={styles.claimItem}>
                  <span style={styles.claimBadge}>CLAIM #{idx + 1}</span> {claim}
                </li>
              ))}
            </ul>
          </div>

          {/* Metrics & Tactics Grid */}
          <div style={styles.grid}>
            {/* Tone & Readability */}
            <div style={styles.card}>
              <h3 style={styles.cardHeader}>SYNTACTIC METRICS</h3>
              <p><strong>Grade Level:</strong> {result.data.readability.grade_level}</p>
              <p><strong>Complexity:</strong> {result.data.readability.complexity}</p>
              <p><strong>Primary Tone:</strong> {result.data.emotional_profile.primary_tone}</p>
            </div>

            {/* Persuasive Tactics */}
            <div style={styles.card}>
              <h3 style={styles.cardHeader}>PERSUASIVE TACTICS DETECTED</h3>
              {Object.entries(result.data.persuasive_tactics).map(([tactic, score], i) => (
                <div key={i} style={styles.tacticRow}>
                  <span>{tactic}</span>
                  <strong>{score}</strong>
                </div>
              ))}
            </div>
          </div>
        </main>
      )}

      {/* Error Output */}
      {result && result.status === 'error' && (
        <div style={styles.errorBox}>
          <strong>ERROR:</strong> {result.message}
        </div>
      )}
    </div>
  )
}

// Vintage Noir Styling Palette
const styles = {
  container: {
    backgroundColor: '#f4f1ea',
    color: '#1a1a1a',
    fontFamily: '"Georgia", "Times New Roman", serif',
    minHeight: '100vh',
    padding: '2rem',
    maxWidth: '900px',
    margin: '0 auto',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2rem',
  },
  topBar: {
    fontSize: '0.8rem',
    letterSpacing: '2px',
    borderBottom: '1px solid #1a1a1a',
    paddingBottom: '4px',
    marginBottom: '1rem',
  },
  title: {
    fontSize: '3.5rem',
    fontWeight: '900',
    letterSpacing: '4px',
    margin: '0',
    fontFamily: '"Playfair Display", "Georgia", serif',
  },
  subTitle: {
    fontStyle: 'italic',
    marginTop: '0.5rem',
    color: '#4a4a4a',
  },
  dividerDouble: {
    borderBottom: '4px double #1a1a1a',
    marginTop: '1rem',
  },
  tabContainer: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '1rem',
  },
  tab: {
    flex: 1,
    padding: '0.6rem',
    backgroundColor: '#e2ddcd',
    border: '1px solid #1a1a1a',
    cursor: 'pointer',
    fontFamily: 'inherit',
    fontWeight: 'bold',
  },
  activeTab: {
    flex: 1,
    padding: '0.6rem',
    backgroundColor: '#1a1a1a',
    color: '#f4f1ea',
    border: '1px solid #1a1a1a',
    cursor: 'pointer',
    fontFamily: 'inherit',
    fontWeight: 'bold',
  },
  inputSection: {
    marginBottom: '2rem',
  },
  textarea: {
    width: '100%',
    height: '140px',
    backgroundColor: '#faf8f5',
    border: '1px solid #1a1a1a',
    padding: '0.8rem',
    fontFamily: 'inherit',
    fontSize: '1rem',
    boxSizing: 'border-box',
    marginBottom: '1rem',
  },
  textInput: {
    width: '100%',
    padding: '0.8rem',
    backgroundColor: '#faf8f5',
    border: '1px solid #1a1a1a',
    fontFamily: 'inherit',
    fontSize: '1rem',
    boxSizing: 'border-box',
    marginBottom: '1rem',
  },
  fileDropZone: {
    border: '2px dashed #1a1a1a',
    padding: '1.5rem',
    textAlign: 'center',
    backgroundColor: '#faf8f5',
    marginBottom: '1rem',
  },
  fileInput: {
    fontFamily: 'inherit',
  },
  fileName: {
    marginTop: '0.5rem',
    fontSize: '0.9rem',
  },
  button: {
    width: '100%',
    padding: '1rem',
    backgroundColor: '#1a1a1a',
    color: '#f4f1ea',
    border: 'none',
    fontSize: '1.1rem',
    letterSpacing: '2px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  buttonDisabled: {
    width: '100%',
    padding: '1rem',
    backgroundColor: '#777',
    color: '#ccc',
    border: 'none',
    fontSize: '1.1rem',
    cursor: 'not-allowed',
  },
  dossier: {
    border: '2px solid #1a1a1a',
    padding: '1.5rem',
    backgroundColor: '#faf8f5',
  },
  dossierHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '2px solid #1a1a1a',
    paddingBottom: '0.5rem',
    marginBottom: '1rem',
  },
  dossierTitle: {
    margin: 0,
    fontSize: '1.5rem',
    letterSpacing: '1px',
  },
  dossierStamp: {
    border: '2px solid #b22222',
    color: '#b22222',
    padding: '2px 8px',
    fontWeight: 'bold',
    fontSize: '0.8rem',
    letterSpacing: '1px',
  },
  metaBox: {
    backgroundColor: '#eef',
    border: '1px solid #99c',
    padding: '0.8rem',
    marginBottom: '1rem',
    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
    fontSize: '0.85rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1rem',
    marginBottom: '1rem',
  },
  card: {
    border: '1px solid #1a1a1a',
    padding: '1rem',
    backgroundColor: '#fff',
  },
  cardHighlight: {
    border: '1px solid #b22222',
    padding: '1rem',
    backgroundColor: '#fffaf8',
  },
  cardHeader: {
    marginTop: 0,
    fontSize: '1rem',
    borderBottom: '1px solid #ccc',
    paddingBottom: '0.3rem',
  },
  cardHeaderAlert: {
    marginTop: 0,
    fontSize: '1rem',
    color: '#b22222',
    borderBottom: '1px solid #fcc',
    paddingBottom: '0.3rem',
  },
  cardText: {
    fontSize: '0.95rem',
    lineHeight: '1.4',
  },
  section: {
    border: '1px solid #1a1a1a',
    padding: '1rem',
    backgroundColor: '#fff',
    marginBottom: '1rem',
  },
  sectionTitle: {
    marginTop: 0,
    fontSize: '1rem',
    borderBottom: '1px solid #ccc',
    paddingBottom: '0.3rem',
  },
  claimsList: {
    paddingLeft: '1rem',
    margin: 0,
  },
  claimItem: {
    marginBottom: '0.5rem',
    fontSize: '0.95rem',
  },
  claimBadge: {
    fontWeight: 'bold',
    fontSize: '0.75rem',
    backgroundColor: '#1a1a1a',
    color: '#fff',
    padding: '2px 5px',
    marginRight: '5px',
  },
  tacticRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.3rem 0',
    borderBottom: '1px dashed #eee',
  },
  errorBox: {
    marginTop: '1rem',
    padding: '1rem',
    backgroundColor: '#fee',
    border: '1px solid #fcc',
    color: '#900',
  }
}

export default App