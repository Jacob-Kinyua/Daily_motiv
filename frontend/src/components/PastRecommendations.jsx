import { useEffect, useState } from 'react';
import { getRecommendations } from '../api.js';

function formatDate(value) {
  try {
    return new Date(value).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return value;
  }
}

export default function PastRecommendations({ user, onBack }) {
  const [recs, setRecs] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    getRecommendations(user.id)
      .then((data) => {
        if (!cancelled) setRecs(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message || 'Couldn\u2019t load your past recommendations.');
      });
    return () => {
      cancelled = true;
    };
  }, [user.id]);

  return (
    <div className="page">
      <button className="back-link" onClick={onBack}>&larr; Back to your file</button>

      <div className="masthead" style={{ textAlign: 'left', marginBottom: 8 }}>
        <span className="eyebrow">The Dossier</span>
        <h1 style={{ fontSize: 30 }}>Past recommendations</h1>
      </div>

      {error && <div className="banner-error">{error}</div>}

      {!error && recs === null && (
        <div className="empty-state">
          <span className="eyebrow">Retrieving your archive&hellip;</span>
        </div>
      )}

      {recs && recs.length === 0 && (
        <div className="empty-state">
          <span className="eyebrow">Nothing filed yet</span>
          <p>Your first dispatch will show up here once it&rsquo;s sent.</p>
        </div>
      )}

      {recs && recs.length > 0 && (
        <div className="rec-list">
          {recs.map((rec) => (
            <div className="card card--filed rec-card" key={rec.id}>
              <div className="rec-card-head">
                <h3>{rec.person_name}</h3>
                <span className="rec-date">{formatDate(rec.sent_at)}</span>
              </div>
              {rec.person_title && <div className="rec-title">{rec.person_title}</div>}
              {rec.fun_fact && <p className="rec-fact">{rec.fun_fact}</p>}
              {Array.isArray(rec.lessons) && rec.lessons.length > 0 && (
                <ul className="rec-lessons">
                  {rec.lessons.map((lesson, i) => (
                    <li key={i}>{lesson}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
