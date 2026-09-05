import { useState } from 'react';

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');

export default function App() {
  const [file, setFile] = useState(null);
  const [job, setJob] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!file) return setError('Choose a PDF or TXT resume first.');
    setLoading(true); setError(''); setResult(null);
    const form = new FormData(); form.append('resume', file); form.append('job_description', job);
    try {
      const response = await fetch(`${API}/analyze`, { method: 'POST', body: form });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Analysis failed.');
      setResult(data);
    } catch (exception) { setError(exception.message === 'Failed to fetch' ? 'The analysis API is unavailable. Please try again shortly.' : exception.message); }
    finally { setLoading(false); }
  }

  return <main>
    <nav><span className="brand">Placement<span>AI</span></span><a href="https://github.com/ANKITJOSHI1605/AI-Placement-Assistant">GitHub ↗</a></nav>
    <section className="hero"><p className="eyebrow">PLACEMENT PREPARATION ASSISTANT</p><h1>Make your resume easier to shortlist.</h1><p>Upload a resume, compare it with a job description, and receive transparent ATS-style feedback.</p></section>
    <section className="workspace">
      <form onSubmit={submit} className="panel">
        <h2>Analyze your resume</h2>
        <label className="drop"><input type="file" accept=".pdf,.txt" onChange={e => setFile(e.target.files[0])}/><strong>{file ? file.name : 'Choose PDF or TXT'}</strong><span>Maximum size: 5 MB</span></label>
        <label>Job description <small>(recommended)</small><textarea rows="9" value={job} onChange={e => setJob(e.target.value)} placeholder="Paste the role description to calculate skill match..." /></label>
        <button disabled={loading}>{loading ? 'Analyzing…' : 'Analyze resume'}</button>
        {error && <p className="error">{error}</p>}
      </form>
      <div className="panel results">
        {!result ? <div className="empty"><div>◎</div><h2>Your report appears here</h2><p>The score is rule-based and explainable—not a guarantee from any employer.</p></div> : <>
          <div className="score"><div><strong>{result.ats_score}</strong><span>/100</span></div><section><p>ATS readiness</p><meter min="0" max="100" value={result.ats_score}/><small>{result.word_count} words · {result.sections_found.length}/5 core sections</small></section></div>
          <div className="grid"><article><span>{result.match_basis === 'role_estimate' ? 'Estimated role match' : 'Job skill match'}</span><strong>{result.match_percentage == null ? 'N/A' : `${result.match_percentage}%`}</strong></article><article><span>Skills found</span><strong>{result.resume_skills.length}</strong></article></div>
          {result.match_note && <p role="status">{result.match_note}</p>}
          <h3>Matched skills</h3><div className="chips good">{result.matched_skills.length ? result.matched_skills.map(x => <span key={x}>{x}</span>) : <p>No job-specific matches yet.</p>}</div>
          <h3>{result.match_basis === 'role_estimate' ? 'Role-baseline skills not detected' : 'Job skills not detected'}</h3><div className="chips">{result.missing_skills.length ? result.missing_skills.map(x => <span key={x}>{x}</span>) : <p>{result.match_percentage == null ? 'No recognized job requirements to compare yet.' : 'No missing skills detected in this comparison.'}</p>}</div>
          <h3>Recommended improvements</h3><ol>{result.recommendations.map(x => <li key={x}>{x}</li>)}</ol>
        </>}
      </div>
    </section>
    <footer>Private by design: uploaded files are analyzed in memory and are not stored.</footer>
  </main>;
}
