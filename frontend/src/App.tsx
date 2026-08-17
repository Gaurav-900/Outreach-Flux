import { useEffect, useState } from 'react'
import type { Session } from '@supabase/supabase-js'
import { supabase } from './lib/supabase'
import Login from './components/Login'
import './App.css'

function App() {
  const [session, setSession] = useState<Session | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [metrics, setMetrics] = useState({
    companies: 0,
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
  const [targetCompanies, setTargetCompanies] = useState<any[]>([])
  const [selectedDraft, setSelectedDraft] = useState<{id: string, subject: string, body: string, to: string} | null>(null)
  const [companyStatusFilter, setCompanyStatusFilter] = useState<string>('ALL')
  const [companySearch, setCompanySearch] = useState<string>('')
  const [timelineStatusFilter, setTimelineStatusFilter] = useState<string>('ALL')
  const [timelineSearch, setTimelineSearch] = useState<string>('')
  const [isSyncing, setIsSyncing] = useState(false)
  const [lastSyncTime, setLastSyncTime] = useState<string>('Never')
  const [nextRunCountdown, setNextRunCountdown] = useState<string>('')

  const fetchDashboardData = async () => {
    try {
      // 1. Fetch generic counts
      const [{ count: companiesCount }, { count: relevantCount }, { count: contactsCount }] = await Promise.all([
        supabase.from('companies').select('*', { count: 'exact', head: true }),
        supabase.from('companies').select('*', { count: 'exact', head: true }).in('outreach_status', ['READY_FOR_OUTREACH', 'DRAFTED', 'APPROVED', 'SENT']),
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
          id, subject, body, status, reply_status, updated_at, error_message,
          companies ( name ),
          contacts ( email )
        `)
        .order('updated_at', { ascending: false })
        .limit(100)

      if (timelineData) setTimeline(timelineData)

      // 4. Fetch last sync time
      const { data: appState } = await supabase.from('app_state').select('value').eq('key', 'last_reply_check').single()
      if (appState && appState.value?.timestamp) {
        const d = new Date(appState.value.timestamp);
        const timeString = d.toLocaleString('en-US', { 
          timeZone: 'UTC', 
          month: 'short', 
          day: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit', 
          second: '2-digit',
          hour12: true 
        });
        setLastSyncTime(`${timeString} UTC`);
      }

      // 5. Fetch Target Companies
      const { data: recentData } = await supabase
        .from('companies')
        .select(`*`)
        .order('created_at', { ascending: false })
        .limit(100)
        
      if (recentData) setTargetCompanies(recentData)

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  const filteredCompanies = targetCompanies.filter(comp => {
    const status = comp.outreach_status || 'NONE';
    const matchesStatus = companyStatusFilter === 'ALL' || status === companyStatusFilter;
    const matchesSearch = companySearch === '' || 
      (comp.name || '').toLowerCase().includes(companySearch.toLowerCase()) || 
      (comp.industry || '').toLowerCase().includes(companySearch.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const filteredTimeline = timeline.filter(row => {
    const matchesStatus = timelineStatusFilter === 'ALL' || row.status === timelineStatusFilter;
    const matchesSearch = timelineSearch === '' || 
      (row.companies?.name || '').toLowerCase().includes(timelineSearch.toLowerCase()) ||
      (row.contacts?.email || '').toLowerCase().includes(timelineSearch.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  useEffect(() => {
    // Check active session immediately
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setAuthLoading(false)
      if (session) {
        fetchDashboardData()
      }
    }).catch((err) => {
      console.error('Failed to get session:', err)
      setAuthLoading(false)
    })

    // Listen for auth changes (login, logout, token refresh)
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, newSession) => {
      console.log('Auth event:', event)
      setSession(newSession)
      
      // If we are no longer loading and we have a session, fetch data
      if (newSession && event === 'SIGNED_IN') {
        fetchDashboardData()
      }
      
      // Ensure loading screen goes away if we receive an event
      setAuthLoading(false)
    })

    const updateCountdown = () => {
      const now = new Date();
      const next = new Date(now);
      if (now.getMinutes() < 30) {
        next.setMinutes(30, 0, 0);
      } else {
        next.setHours(now.getHours() + 1, 0, 0, 0);
      }
      
      const diff = next.getTime() - now.getTime();
      const minutes = Math.floor(diff / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      setNextRunCountdown(`${minutes}m ${seconds}s`);
    };
    
    updateCountdown();
    const timerInterval = setInterval(updateCountdown, 1000);

    return () => {
      subscription.unsubscribe();
      clearInterval(timerInterval);
    }
  }, [])

  const handleSyncReplies = async () => {
    setIsSyncing(true)
    try {
      if (!session) throw new Error('Not authenticated');
      
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      const res = await fetch(`${apiUrl}/api/replies/sync`, { 
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      })
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

  const handleApprove = async (id: string) => {
    try {
      const { error } = await supabase
        .from('outreach')
        .update({ status: 'APPROVED' })
        .eq('id', id);
        
      if (error) throw error;
      
      // Trigger the backend to process the sending queue immediately
      if (session) {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
        await fetch(`${apiUrl}/api/outreach/trigger-sending`, { 
          method: 'POST',
          headers: { 'Authorization': `Bearer ${session.access_token}` }
        }).catch(err => console.error('Failed to trigger sending:', err));
      }
      
      await fetchDashboardData();
    } catch (error) {
      console.error('Failed to approve draft:', error);
      alert('Failed to approve draft.');
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut();
  }

  if (authLoading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'var(--text)' }}>Loading OutreachFlow...</div>;
  }

  if (!session) {
    return <Login />;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>AI Outreach Dashboard</h1>
        <div className="sync-controls">
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', fontSize: '0.85rem', color: 'var(--text-muted)', marginRight: '1rem' }}>
            <span>Last check: {lastSyncTime}</span>
            <span>Next auto-run in: {nextRunCountdown}</span>
          </div>
          <button 
            className="sync-button" 
            onClick={handleSyncReplies} 
            disabled={isSyncing}
          >
            {isSyncing ? 'Checking Gmail...' : 'Refresh Replies'}
          </button>
          <button 
            onClick={handleLogout} 
            className="btn-logout"
          >
            Logout
          </button>
        </div>
      </header>

      <section className="metrics-grid">
        <div className="metric-card">
          <h3>Discovery</h3>
          <ul>
            <li>Companies Found: <strong>{metrics.companies}</strong></li>
            <li>Targeted for Outreach: <strong>{metrics.relevant}</strong></li>
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

      <section className="timeline-section" style={{ marginBottom: '3rem' }}>
        <div className="section-header-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
          <h2 style={{ margin: 0 }}>Outreach Timeline</h2>
          <div className="table-filter-bar" style={{ display: 'flex', gap: '0.8rem' }}>
            <input 
              type="text" 
              placeholder="Search email, company, title..." 
              value={timelineSearch}
              onChange={e => setTimelineSearch(e.target.value)}
              className="filter-input"
            />
            <select 
              value={timelineStatusFilter} 
              onChange={e => setTimelineStatusFilter(e.target.value)}
              className="filter-select"
            >
              <option value="ALL">All Statuses</option>
              <option value="DRAFT">Draft</option>
              <option value="APPROVED">Approved</option>
              <option value="SENT">Sent</option>
              <option value="FAILED">Failed</option>
            </select>
          </div>
        </div>
        <div className="table-container">
          <table className="timeline-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Company</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Reply Status</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTimeline.length === 0 ? (
                <tr><td colSpan={7} style={{textAlign: 'center'}}>No matching outreach records found.</td></tr>
              ) : (
                filteredTimeline.map((row) => (
                  <tr key={row.id}>
                    <td>{new Date(row.updated_at).toLocaleDateString()}</td>
                    <td>{row.companies?.name || 'Unknown'}</td>
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
                    <td>
                      {row.status === 'DRAFT' && (
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <button 
                            className="btn-view"
                            onClick={() => setSelectedDraft({id: row.id, subject: row.subject, body: row.body, to: row.contacts?.email || 'Hiring Team'})}
                          >
                            View
                          </button>
                          <button 
                            className="btn-approve"
                            onClick={() => handleApprove(row.id)}
                          >
                            Approve
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="recent-section">
        <div className="section-header-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
          <h2 style={{ margin: 0 }}>Target Companies</h2>
          <div className="table-filter-bar" style={{ display: 'flex', gap: '0.8rem' }}>
            <input 
              type="text" 
              placeholder="Search company or industry..." 
              value={companySearch}
              onChange={e => setCompanySearch(e.target.value)}
              className="filter-input"
            />
            <select 
              value={companyStatusFilter} 
              onChange={e => setCompanyStatusFilter(e.target.value)}
              className="filter-select"
            >
              <option value="ALL">All Statuses</option>
              <option value="NONE">None</option>
              <option value="READY_FOR_OUTREACH">Ready</option>
              <option value="DRAFTED">Drafted</option>
              <option value="APPROVED">Approved</option>
            </select>
          </div>
        </div>
        <div className="table-container">
          <table className="recent-table">
            <thead>
              <tr>
                <th>Discovered</th>
                <th>Company</th>
                <th>Industry</th>
                <th>Status</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {filteredCompanies.length === 0 ? (
                <tr><td colSpan={5} style={{textAlign: 'center'}}>No matching companies found.</td></tr>
              ) : (
                filteredCompanies.map((comp) => {
                  const status = comp.outreach_status || 'NONE';
                  return (
                    <tr key={comp.id}>
                      <td>{new Date(comp.created_at).toLocaleDateString()}</td>
                      <td><strong>{comp.name}</strong></td>
                      <td>{comp.industry || '-'}</td>
                      <td>
                        <span className={`badge status-${status.toLowerCase()}`}>
                          {status}
                        </span>
                      </td>
                      <td>
                        {comp.website ? (
                          <a href={comp.website} target="_blank" rel="noopener noreferrer" style={{color: 'var(--accent)', textDecoration: 'none'}}>Visit Site</a>
                        ) : '-'}
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </section>



      {selectedDraft && (
        <div className="modal-overlay" onClick={() => setSelectedDraft(null)}>
          <div className="email-client-modal" onClick={e => e.stopPropagation()}>
            <div className="email-header">
              <div className="email-header-top">
                <h3>New Message</h3>
                <button className="modal-close" onClick={() => setSelectedDraft(null)}>×</button>
              </div>
              <div className="email-meta">
                <div className="email-meta-row">
                  <span className="meta-label">To</span>
                  <span className="meta-value">{selectedDraft.to}</span>
                </div>
                <div className="email-meta-row">
                  <span className="meta-label">From</span>
                  <span className="meta-value">Gaurav Sharma &lt;worksforgauravsharma@gmail.com&gt;</span>
                </div>
                <div className="email-meta-row subject-row">
                  <span className="meta-label">Subject</span>
                  <span className="meta-value subject-value">{selectedDraft.subject}</span>
                </div>
              </div>
            </div>
            <div className="email-body">
              {selectedDraft.body}
            </div>
            <div className="email-footer">
              <button className="btn-send-email" onClick={() => {
                handleApprove(selectedDraft.id);
                setSelectedDraft(null);
              }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{marginRight: '8px'}}><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                Approve & Send
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
