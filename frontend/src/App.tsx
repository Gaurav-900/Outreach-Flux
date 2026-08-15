import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'
import './App.css'

function App() {
  const [metrics, setMetrics] = useState({
    companies: 0,
    opportunities: 0,
    relevant: 0,
    contacts: 0,
    drafts: 0,
    sent: 0,
    failed: 0,
    humanReplies: 0,
    autoReplies: 0,
    pendingReplies: 0,
  })

  const [timeline, setTimeline] = useState<any[]>([])
  const [isSyncing, setIsSyncing] = useState(false)
  const [lastSyncTime, setLastSyncTime] = useState<string>('Never')

  const fetchDashboardData = async () => {
    try {
      // 1. Fetch generic counts
      const [{ count: companiesCount }, { count: oppsCount }, { count: relevantCount }, { count: contactsCount }] = await Promise.all([
        supabase.from('companies').select('*', { count: 'exact', head: true }),
        supabase.from('opportunities').select('*', { count: 'exact', head: true }),
        supabase.from('opportunities').select('*', { count: 'exact', head: true }).in('status', ['READY_FOR_OUTREACH', 'DRAFTED']),
        supabase.from('contacts').select('*', { count: 'exact', head: true })
      ])

      // 2. Fetch outreach counts
      const { data: outreachData } = await supabase.from('outreach').select('status, reply_status')
      
      let drafts = 0, sent = 0, failed = 0, human = 0, auto = 0, pending = 0;
      
      outreachData?.forEach(row => {
        if (['DRAFT', 'QUEUED', 'APPROVED', 'AUTO_APPROVED'].includes(row.status)) drafts++;
        if (row.status === 'SENT') sent++;
        if (row.status === 'FAILED') failed++;
        
        if (row.status === 'SENT') {
          if (row.reply_status === 'HUMAN_REPLY') human++;
          else if (row.reply_status === 'AUTO_REPLY') auto++;
          else pending++;
        }
      })

      setMetrics({
        companies: companiesCount || 0,
        opportunities: oppsCount || 0,
        relevant: relevantCount || 0,
        contacts: contactsCount || 0,
        drafts, sent, failed,
        humanReplies: human,
        autoReplies: auto,
        pendingReplies: pending
      })

      // 3. Fetch Timeline (Outreach joined with companies/opportunities)
      const { data: timelineData } = await supabase
        .from('outreach')
        .select(`
          id, subject, status, reply_status, updated_at, error_message,
          companies ( name ),
          opportunities ( title ),
          contacts ( email )
        `)
        .order('updated_at', { ascending: false })
        .limit(20)

      if (timelineData) setTimeline(timelineData)

      // 4. Fetch last sync time
      const { data: appState } = await supabase.from('app_state').select('value').eq('key', 'last_reply_check').single()
      if (appState && appState.value?.timestamp) {
        setLastSyncTime(new Date(appState.value.timestamp).toLocaleString())
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const handleSyncReplies = async () => {
    setIsSyncing(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const res = await fetch(`${apiUrl}/api/replies/sync`, { method: 'POST' })
      const data = await res.json()
      console.log('Sync result:', data)
      await fetchDashboardData()
    } catch (error) {
      console.error('Sync failed', error)
      alert('Failed to sync replies. Make sure backend is running.')
    } finally {
      setIsSyncing(false)
    }
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>AI Outreach Dashboard</h1>
        <div className="sync-controls">
          <span className="last-sync">Last check: {lastSyncTime}</span>
          <button 
            className="sync-button" 
            onClick={handleSyncReplies} 
            disabled={isSyncing}
          >
            {isSyncing ? 'Checking Gmail...' : 'Refresh Replies'}
          </button>
        </div>
      </header>

      <section className="metrics-grid">
        <div className="metric-card">
          <h3>Discovery</h3>
          <ul>
            <li>Companies Found: <strong>{metrics.companies}</strong></li>
            <li>Jobs Found: <strong>{metrics.opportunities}</strong></li>
            <li>Relevant Opportunities: <strong>{metrics.relevant}</strong></li>
            <li>Contacts Discovered: <strong>{metrics.contacts}</strong></li>
          </ul>
        </div>
        
        <div className="metric-card">
          <h3>Pipeline</h3>
          <ul>
            <li>Pending Drafts: <strong>{metrics.drafts}</strong></li>
            <li>Successfully Sent: <strong>{metrics.sent}</strong></li>
            <li>Failed Sends: <strong style={{color: 'red'}}>{metrics.failed}</strong></li>
          </ul>
        </div>

        <div className="metric-card">
          <h3>Replies</h3>
          <ul>
            <li>Human Replies: <strong style={{color: '#4CAF50'}}>{metrics.humanReplies}</strong></li>
            <li>Automated Replies: <strong>{metrics.autoReplies}</strong></li>
            <li>Awaiting Reply: <strong>{metrics.pendingReplies}</strong></li>
          </ul>
        </div>
      </section>

      <section className="timeline-section">
        <h2>Outreach Timeline</h2>
        <div className="table-container">
          <table className="timeline-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Reply Status</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {timeline.length === 0 ? (
                <tr><td colSpan={7} style={{textAlign: 'center'}}>No outreach records found.</td></tr>
              ) : (
                timeline.map((row) => (
                  <tr key={row.id}>
                    <td>{new Date(row.updated_at).toLocaleDateString()}</td>
                    <td>{row.companies?.name || 'Unknown'}</td>
                    <td>{row.opportunities?.title || 'Unknown'}</td>
                    <td>{row.contacts?.email || 'N/A'}</td>
                    <td>
                      <span className={`badge status-${row.status.toLowerCase()}`}>
                        {row.status}
                      </span>
                    </td>
                    <td>
                      {row.status === 'SENT' ? (
                        <span className={`badge reply-${row.reply_status.toLowerCase()}`}>
                          {row.reply_status}
                        </span>
                      ) : '-'}
                    </td>
                    <td className="error-text">{row.error_message || ''}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default App
