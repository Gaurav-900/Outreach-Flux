import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [healthStatus, setHealthStatus] = useState<string>('Checking backend...')

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/health`)
        const data = await response.json()
        setHealthStatus(data.message)
      } catch (error) {
        setHealthStatus('Backend is offline or unreachable')
        console.error(error)
      }
    }
    
    checkHealth()
  }, [])

  return (
    <>
      <h1>AI Job Outreach Assistant</h1>
      <div className="card">
        <p>Backend Status: <strong>{healthStatus}</strong></p>
      </div>
      <p className="read-the-docs">
        Phase 0 Foundation Setup
      </p>
    </>
  )
}

export default App
